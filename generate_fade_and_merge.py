import subprocess
import sys
import os

# === PARAMÈTRES À ADAPTER ===
video_file = "media/videos/infinite_product/1920p60/ShortsManual.mp4"  # ta vidéo short
input_music = "music.mp3"         # musique d'origine
fade_duration = 3                   # durée du fondu en secondes
output_music = "music_fade.mp3"   # musique générée avec fade-out
final_video = "ShortsManual_with_music.mp4"  # vidéo finale avec musique intégrée

# --- Vérif que la vidéo existe ---
if not os.path.exists(video_file):
    print(f" Erreur : vidéo '{video_file}' introuvable")
    sys.exit(1)

# --- Lire la durée exacte de la vidéo ---
result = subprocess.run(
    [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        video_file
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
try:
    short_duration = float(result.stdout.strip())
except ValueError:
    print("Erreur : impossible de lire la durée de la vidéo.")
    sys.exit(1)

fade_start = max(short_duration - fade_duration, 0)
print(f"⏱ Durée vidéo : {short_duration:.2f} sec")
print(f" Fade-out : start={fade_start:.2f}s, durée={fade_duration}s")

# --- Génération musique avec fade-out ---
subprocess.run([
    "ffmpeg",
    "-i", input_music,
    "-af", f"afade=t=out:st={fade_start}:d={fade_duration}",
    "-t", str(short_duration),
    output_music,
    "-y"
], check=True)
print(f"Musique générée : {output_music}")

# --- Fusionner musique + vidéo ---
subprocess.run([
    "ffmpeg",
    "-i", video_file,
    "-i", output_music,
    "-c:v", "copy",      # copie la vidéo sans recompression
    "-map", "0:v:0",     # piste vidéo depuis le fichier vidéo
    "-map", "1:a:0",     # piste audio depuis le fichier musique
    "-shortest",         # coupe si musique > vidéo
    final_video,
    "-y"
], check=True)

print(f" Vidéo finale exportée : {final_video}")
