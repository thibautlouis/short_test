# e.g python generate.py doppler --music_path /Users/louisthibaut/Desktop/projects/math_video/Music/Kyoto.mp3

import os
import sys
import shutil
import math, tempfile, os
import subprocess
import importlib.util
import textwrap
from pathlib import Path

# --- Music (moviepy) ---
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
from pydub import AudioSegment

# -------- Réglages par défaut --------
DEFAULT_LANGS = ["FR", "EN", "ES", "PT"]
DEFAULT_SCENE = "ShortsManual"   # la Scene à rendre dans <slug>.py
QUALITY = "-qk"                  # -pqh (preview) ou -qk (1080p)

ROOT       = Path(__file__).parent.resolve()
RAW_DIR    = ROOT / "shorts" / "videos" / "raw"      # rendu temporaire
VIDEO_DIR  = ROOT / "shorts" / "videos"              # .mp4 finaux
META_DIR   = ROOT / "shorts" / "metadata"            # .txt YouTube
THUMBS_DIR = ROOT / "shorts" / "thumbs"              # PNG title cards

# -------- Utils --------
def load_metadata(slug):
    meta_path = ROOT / f"{slug}_metadata.py"
    if not meta_path.exists():
        raise FileNotFoundError(f"{slug}_metadata.py not found in {ROOT}")
    spec = importlib.util.spec_from_file_location("metadata", meta_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    for key in ("TITLES", "DESCR", "HASHTAGS"):
        if not hasattr(mod, key):
            raise ValueError(f"{slug}_metadata.py must define TITLES, DESCR, HASHTAGS")
    return mod

def write_metadata_txt(slug: str, lang: str, meta_mod):
    META_DIR.mkdir(parents=True, exist_ok=True)
    title    = meta_mod.TITLES[lang]
    descr    = textwrap.dedent(meta_mod.DESCR[lang]).strip()
    hashtags = meta_mod.HASHTAGS[lang]
    (META_DIR / f"{slug}_{lang}.txt").write_text(
        f"{title}\n\n{descr}\n\n{hashtags}", encoding="utf-8"
    )

def clear_raw_dir():
    if RAW_DIR.exists():
        shutil.rmtree(RAW_DIR)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

def find_rendered_mp4(media_root: Path, out_name: str) -> Path | None:
    for p in media_root.rglob(f"{out_name}.mp4"):
        return p
    return None


def add_music_with_fade_and_offset(video_path: Path,
                                   music_path: Path,
                                   output_path: Path,
                                   start_offset: float = 2.0,    # music starts after 4s
                                   fade_out_duration: float = 4.0,
                                   volume: float = 0.8):
    """Mix music under the video: start at offset, trim to video length, and fade out at the end."""
    video = VideoFileClip(str(video_path))
    vid_dur = float(video.duration)
    fps = getattr(video, "fps", 30) or 30

    play_dur = max(0.0, vid_dur - start_offset)
    if play_dur <= 0.05:
        # Too short to bother mixing
        video.write_videofile(str(output_path), codec="libx264", audio_codec="aac", fps=fps)
        video.close()
        return

    # --- Build processed music with pydub (volume + fade + exact length) ---
    seg = AudioSegment.from_file(str(music_path))
    # scale linear volume to dB
    gain_db = 0.0 if volume <= 0 else 20.0 * math.log10(volume)
    seg = seg.apply_gain(gain_db)
    seg = seg[:int(play_dur * 1000)]  # trim to useful duration
    if fade_out_duration > 0:
        seg = seg.fade_out(int(min(fade_out_duration, play_dur) * 1000))

    # export to a temp wav
    tmpdir = tempfile.mkdtemp(prefix="mix_")
    tmp_wav = os.path.join(tmpdir, "music_processed.wav")
    seg.export(tmp_wav, format="wav")

    # --- Place music at start_offset and mux with MoviePy ---
    music_clip = AudioFileClip(tmp_wav).with_start(start_offset)
    final_audio = CompositeAudioClip([music_clip])   # (add more tracks here if needed)
    final_video = video.with_audio(final_audio)

    tmp_out = output_path.with_suffix(".music.tmp.mp4")
    final_video.write_videofile(str(tmp_out), codec="libx264", audio_codec="aac", audio_bitrate="320k", fps=fps)

    # cleanup & swap
    final_audio.close(); music_clip.close(); video.close()
    if Path(tmp_wav).exists():
        try: os.remove(tmp_wav)
        except: pass
    try: os.rmdir(tmpdir)
    except: pass
    if output_path.exists(): output_path.unlink()
    tmp_out.rename(output_path)


# -----------------------

# -------- Rendu Manim (vidéo principale) --------
def render_one(slug: str, scene: str, lang: str) -> Path:
    script_path = ROOT / f"{slug}.py"
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    out_name = f"{slug}_{lang}"
    media_dir = RAW_DIR / slug / lang
    media_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["SHORT_LANG"] = lang  # lu par ton lang.py

    cmd = [
        "./manim",
        QUALITY,
        "--fps", "30",            # stable pour Shorts
        str(script_path), scene,
        "-o", out_name,
        "--media_dir", str(media_dir),
    ]
    print("==> render:", " ".join(cmd))
    subprocess.run(cmd, check=True, env=env)

    produced = find_rendered_mp4(media_root=media_dir, out_name=out_name)
    if not produced:
        raise FileNotFoundError(f"Rendered file not found under {media_dir}")

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    target = VIDEO_DIR / f"{out_name}.mp4"
    if target.exists():
        target.unlink()
    shutil.move(str(produced), str(target))
    print(f"Saved video: {target}")
    return target

# -------- Title card (image PNG via Manim) --------
def render_title_card(slug: str, lang: str) -> Path:
    THUMBS_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["SHORT_LANG"] = lang

    out_png_name = f"{slug}_title_{lang}.png"
    out_png_path = THUMBS_DIR / out_png_name

    cmd = [
        "./manim", "-qk",
        f"{slug}_title_card.py", "TitleCard",
        "--media_dir", str(THUMBS_DIR),
        "--custom_folders",             # pas de sous-dossiers images/<script>
        "--output_file", out_png_name,  # PNG écrit directement dans THUMBS_DIR
    ]
    print("==> title card:", " ".join(cmd))
    subprocess.run(cmd, check=True, env=env)

    if not out_png_path.exists():
        raise FileNotFoundError(f"Title card PNG not found: {out_png_path}")
    print(f"Saved title card: {out_png_path}")
    return out_png_path

# -------- Main CLI --------
def main():
    """
    Usage:
      python generate.py <slug> [LANGS...] [--scene SceneName] [--quality -pqh|-qk] [--no-thumb] [--music_path /path/music.mp3]

    Exemples:
      python generate.py infinite_product
      python generate.py infinite_product EN PT --scene ShortsManual --quality -pqh
      python generate.py infinite_product --music_path assets/music.mp3
    """
    if len(sys.argv) < 2:
        print("Usage: python generate.py <slug> [LANGS...] [--scene SceneName] [--quality -pqh|-qk] [--no-thumb] [--music_path /path/music.mp3]")
        sys.exit(1)

    slug = sys.argv[1]
    scene = DEFAULT_SCENE
    langs = []
    make_thumb = True
    music_path = None  # --- Music (moviepy) ---

    args = sys.argv[2:]
    i = 0
    global QUALITY
    while i < len(args):
        a = args[i]
        if a == "--scene" and i + 1 < len(args):
            scene = args[i + 1]; i += 2
        elif a == "--quality" and i + 1 < len(args):
            QUALITY = args[i + 1]; i += 2
        elif a == "--no-thumb":
            make_thumb = False; i += 1
        elif a == "--music_path" and i + 1 < len(args):  # --- Music (moviepy) ---
            music_path = args[i + 1]; i += 2
        else:
            langs.append(a); i += 1

    langs = langs or DEFAULT_LANGS
    meta = load_metadata(slug)
    clear_raw_dir()

    for lang in langs:
        # 1) vidéo
        final_mp4 = render_one(slug, scene, lang)

        # 1bis) musique (optionnelle) — démarre à 4s, fade 2s, volume 0.8
        if music_path and Path(music_path).exists():
            tmp_out = final_mp4.with_suffix(".music.mp4")
            add_music_with_fade_and_offset(
                video_path=final_mp4,
                music_path=Path(music_path),
                output_path=tmp_out,
        # defaults: start_offset=4.0, fade_out=2.0, volume=0.8
            )
            final_mp4.unlink()
            tmp_out.rename(final_mp4)

        # 2) miniature PNG (optionnel)
        if make_thumb:
            render_title_card(slug, lang)
        # 3) métadonnées
        write_metadata_txt(slug, lang, meta)

    print("Done.")
    print(f"Videos   → {VIDEO_DIR}")
    print(f"Metadata → {META_DIR}")
    if make_thumb:
        print(f"Title cards → {THUMBS_DIR}")

if __name__ == "__main__":
    main()
