
# doppler_galaxy_pygame_export.py
# -*- coding: utf-8 -*-
"""
Redshift — onde uniforme + grille comobile + Hubble exact (galaxie attachée à la grille)
Version export (PNG + ProRes 4444 MOV). Grille SSAA ancrée sur l'observateur.
"""

import os
import sys
import math
import pygame
from math import ceil

# ---------- Paramètres généraux ----------
SIZE = 800
WIDTH, HEIGHT = SIZE, SIZE

# Assets (placez galaxy.png et terre.png à côté de ce script)
IMG_PATH = os.path.join(os.path.dirname(__file__), "galaxy.png")   # galaxie
EARTH_IMG_PATH = os.path.join(os.path.dirname(__file__), "terre.png")  # Terre

# Cosmologie (pédagogique)
H = 0.16                 # constante de Hubble (pédagogique)
LAMBDA_EMIT_PX0 = 22     # λ émise (pixels)
AMP = 22                 # amplitude onde (pixels)

# Étirement (modéré)
STRETCH_GAIN  = 0.0035   # z = gain * D
STRETCH_POWER = 1.05     # λ_obs = λ_emit * (1+z)^power

# Grille comobile
GRID_BASE_SPACING = 60.0
GRID_ALPHA  = 100
GRID_LINE_WIDTH = 2

# --- Grille anti-scintillement (SSAA + scale ancré sur p_obs) ---
_SSAA = 2
_grid_base_surface = None

def _ensure_base_grid(p_obs):
    """Construit une grille de référence haute résolution, ancrée sur p_obs."""
    global _grid_base_surface
    if _grid_base_surface is not None:
        return
    w2, h2 = WIDTH * _SSAA, HEIGHT * _SSAA
    surf = pygame.Surface((w2, h2), pygame.SRCALPHA)

    col = (180, 180, 180, GRID_ALPHA)
    spacing = int(round(GRID_BASE_SPACING * _SSAA))

    ox = int(round(p_obs[0] * _SSAA))
    oy = int(round(p_obs[1] * _SSAA))

    # Lignes verticales
    x = ox
    while x <= w2:
        pygame.draw.line(surf, col, (x, 0), (x, h2), GRID_LINE_WIDTH)
        x += spacing
    x = ox - spacing
    while x >= 0:
        pygame.draw.line(surf, col, (x, 0), (x, h2), GRID_LINE_WIDTH)
        x -= spacing

    # Lignes horizontales
    y = oy
    while y <= h2:
        pygame.draw.line(surf, col, (0, y), (w2, y), GRID_LINE_WIDTH)
        y += spacing
    y = oy - spacing
    while y >= 0:
        pygame.draw.line(surf, col, (0, y), (w2, y), GRID_LINE_WIDTH)
        y -= spacing

    _grid_base_surface = surf

def draw_expanding_grid(surface, origin, a):
    """Dessine la grille comobile en redimensionnant la grille de référence autour de origin."""
    _ensure_base_grid(origin)

    s = max(0.05, float(a))  # facteur d'échelle

    tw = max(1, int(round(WIDTH * s)))
    th = max(1, int(round(HEIGHT * s)))

    grid_scaled = pygame.transform.smoothscale(_grid_base_surface, (tw, th))

    # Conserver origin fixe: TL = (1 - s) * origin
    tlx = int(round((1.0 - s) * origin[0]))
    tly = int(round((1.0 - s) * origin[1]))

    surface.blit(grid_scaled, (tlx, tly))

# ---------- Export (frames + masters) ----------
RECORD_PNG = True
RECORD_MP4 = False  # web MP4 off by default; ProRes master on
RECORD_FPS = 30
RECORD_DIR = os.path.join(os.path.dirname(__file__), "export_frames_galaxy")
RECORD_MP4_PATH = os.path.join(os.path.dirname(__file__), "doppler_galaxy.mp4")
PRORES_MASTER = True
PRORES_MOV_PATH = os.path.join(os.path.dirname(__file__), "doppler_galaxy_prores4444.mov")
DURATION_S = 10.0   # durée totale (s)

# ---------- Utilitaires ----------
def load_image_small(path):
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_size()
    w2, h2 = max(1, w//8), max(1, h//8)  # galaxie petite
    return pygame.transform.smoothscale(img, (w2, h2))

def load_earth_icon(path, max_diameter=200):
    """Charge l'image de la Terre en conservant le ratio, insérée dans un carré max_diameter."""
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_size()
    scale = max_diameter / float(max(w, h))
    new_size = (int(w * scale), int(h * scale))
    return pygame.transform.smoothscale(img, new_size)

# --- Onde sinusoïdale ---
WAVE_DS = 3.0

def draw_wave_uniform(surface, p_obs, p_gal, amp, lam_px, phase0, color):
    x1, y1 = p_obs
    x2, y2 = p_gal
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L < 2:
        return
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    k = 2 * math.pi / max(lam_px, 1e-6)

    pts, phi, s = [], phase0, 0.0
    while s <= L:
        phi += k * WAVE_DS
        off = amp * math.sin(phi)
        x = x1 + ux * s + nx * off
        y = y1 + uy * s + ny * off
        pts.append((int(x), int(y)))
        s += WAVE_DS

    if len(pts) >= 2:
        pygame.draw.aalines(surface, color, False, pts)

# ---------- Assemblage vidéo robuste ----------
def _assemble_video_from_frames(frames_dir, mp4_path, fps):
    """Try several backends to create MP4. If all fail, print an ffmpeg command."""
    import os

    # 1) imageio with libx264 + yuv420p
    try:
        import imageio.v2 as imageio
        frames = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(".png")])
        if frames:
            with imageio.get_writer(mp4_path, fps=fps, codec='libx264', quality=8, format='FFMPEG', output_params=['-pix_fmt', 'yuv420p']) as writer:
                for fname in frames:
                    writer.append_data(imageio.imread(os.path.join(frames_dir, fname)))
        print(f"[imageio/libx264] MP4 écrit : {mp4_path} ({len(frames)} frames)")
        return True
    except Exception as e:
        print("[imageio/libx264] échec :", e)

    # 2) imageio with mpeg4
    try:
        import imageio.v2 as imageio
        frames = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(".png")])
        if frames:
            with imageio.get_writer(mp4_path, fps=fps, codec='mpeg4', quality=8, format='FFMPEG') as writer:
                for fname in frames:
                    writer.append_data(imageio.imread(os.path.join(frames_dir, fname)))
        print(f"[imageio/mpeg4] MP4 écrit : {mp4_path} ({len(frames)} frames)")
        return True
    except Exception as e:
        print("[imageio/mpeg4] échec :", e)

    # 3) OpenCV fallback
    try:
        import cv2
        import imageio.v2 as imageio
        frames = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(".png")])
        if not frames:
            raise RuntimeError("Aucune frame PNG trouvée.")
        first = imageio.imread(os.path.join(frames_dir, frames[0]))
        h, w = first.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        vw = cv2.VideoWriter(mp4_path, fourcc, fps, (w, h))
        if not vw.isOpened():
            raise RuntimeError("OpenCV VideoWriter non disponible.")
        for fname in frames:
            img = imageio.imread(os.path.join(frames_dir, fname))
            if img.shape[2] == 4:
                img = img[:, :, :3]  # drop alpha
            import cv2 as _cv2
            vw.write(_cv2.cvtColor(img, _cv2.COLOR_RGB2BGR))
        vw.release()
        print(f"[OpenCV/mp4v] MP4 écrit : {mp4_path} ({len(frames)} frames)")
        return True
    except Exception as e:
        print("[OpenCV/mp4v] échec :", e)

    # 4) Print ffmpeg command
    cmd = f'ffmpeg -y -framerate {fps} -i "{frames_dir}/frame_%05d.png" -c:v libx264 -pix_fmt yuv420p "{mp4_path}"'
    print("Aucun backend n'a réussi. Essayez :", cmd)
    return False

def _assemble_prores_from_frames(frames_dir, mov_path, fps):
    """Assemble frames into a ProRes 4444 (10-bit with alpha) master using ffmpeg (prores_ks)."""
    import os, shutil, subprocess

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        cmd = f'ffmpeg -y -framerate {fps} -start_number 0 -i "{frames_dir}/frame_%05d.png" -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le "{mov_path}"'
        print("ffmpeg introuvable. Assemblez manuellement avec :")
        print(cmd)
        return False

    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-start_number", "0",
        "-i", f"{frames_dir}/frame_%05d.png",
        "-c:v", "prores_ks",
        "-profile:v", "4",
        "-pix_fmt", "yuva444p10le",
        mov_path
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"[ffmpeg/prores4444] MOV écrit : {mov_path}")
        return True
    except Exception as e:
        print("Échec ffmpeg prores_ks :", e)
        print("Essayez manuellement :", ' '.join(cmd))
        return False

# ---------- Programme principal ----------
def main():
    pygame.init()
    pygame.display.set_caption("Redshift — comobile (export, grille stable)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Assets
    if not os.path.exists(IMG_PATH):
        print("Image galaxie introuvable :", IMG_PATH); sys.exit(1)
    if not os.path.exists(EARTH_IMG_PATH):
        print("Image Terre introuvable :", EARTH_IMG_PATH); sys.exit(1)

    galaxy = load_image_small(IMG_PATH)

    # Observateur (origine de la grille)
    p_obs = (int(0.15 * WIDTH), int(0.85 * HEIGHT))
    earth = load_earth_icon(EARTH_IMG_PATH, max_diameter=120)

    # Galaxie sur un nœud comobile (multiples du pas de grille)
    nx_cells, ny_cells = 3, -3
    r_com = (nx_cells * GRID_BASE_SPACING, ny_cells * GRID_BASE_SPACING)
    r_com_norm = math.hypot(*r_com)

    # Timeline déterministe pour l'export
    dt = 1.0 / RECORD_FPS
    total_frames = ceil(DURATION_S * RECORD_FPS)

    # Export (dossier frames reset)
    if RECORD_PNG or RECORD_MP4 or PRORES_MASTER:
        os.makedirs(RECORD_DIR, exist_ok=True)
        for f in os.listdir(RECORD_DIR):
            if f.lower().endswith(".png"):
                try:
                    os.remove(os.path.join(RECORD_DIR, f))
                except Exception:
                    pass

    t = 0.0
    phase = 0.0

    for frame_idx in range(total_frames):
        # Gestion événements pour rester responsive
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return

        # Temps simulé exact de la frame
        t = frame_idx * dt

        # Facteur d'échelle comobile partagé (grille & galaxie)
        a = math.exp(H * t)

        # Position physique de la galaxie
        gal_x = p_obs[0] + a * r_com[0]
        gal_y = p_obs[1] + a * r_com[1]
        p_gal = (gal_x, gal_y)

        # Distance & redshift
        D = a * r_com_norm
        z = STRETCH_GAIN * D
        lam_px = LAMBDA_EMIT_PX0 * (1.0 + z) ** STRETCH_POWER

        # Couleur: blanc -> rouge léger (transition douce)
        
        
        COLOR_FADE_S = 5.0
        aa = min(1.0, max(0.0, t / COLOR_FADE_S))
        # easing (smoothstep) pour une transition douce
        tcol = aa * aa * (3 - 2 * aa)
        color = (255, int(255 - (255-80) * tcol), int(255 - (255-80) * tcol))


       # tcol = min(0.2, z / 1.0)
       # color = (
       #     255,
       #     int(255 - (255-80) * tcol),
       #     int(255 - (255-80) * tcol)
       # )

        # Propagation (galaxie -> Terre)
        phase += 6.0 * dt

        # --- Rendu ---
        screen.fill((0, 0, 0))
        draw_expanding_grid(screen, p_obs, a)

        # Terre (observateur) : centrée sur p_obs
        earth_rect = earth.get_rect(center=p_obs)
        screen.blit(earth, earth_rect)

        # Onde
        draw_wave_uniform(screen, p_obs, p_gal, AMP, lam_px, phase, color)

        # Galaxie
        grect = galaxy.get_rect(center=(int(gal_x), int(gal_y)))
        screen.blit(galaxy, grect)

        pygame.display.flip()
        clock.tick(120)

        # Export frame
        if RECORD_PNG or PRORES_MASTER or RECORD_MP4:
            out_path = os.path.join(RECORD_DIR, f"frame_{frame_idx:05d}.png")
            try:
                pygame.image.save(screen, out_path)
            except Exception:
                pass

    # Fin pygame
    pygame.quit()

    # Assemblage ProRes 4444 (master)
    if PRORES_MASTER:
        ok_prores = _assemble_prores_from_frames(RECORD_DIR, PRORES_MOV_PATH, RECORD_FPS)
        if not ok_prores:
            print('ProRes non généré automatiquement — utilisez la commande ffmpeg affichée ci-dessus.')

    # Optionnel : version web MP4
    if RECORD_MP4:
        ok = _assemble_video_from_frames(RECORD_DIR, RECORD_MP4_PATH, RECORD_FPS)
        if not ok:
            print('Échec MP4 automatique — frames PNG disponibles pour assemblage manuel avec ffmpeg.')

if __name__ == "__main__":
    main()
