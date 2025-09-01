#python cow_enclosures.py --export sortie_frames/sortie.mp4 --duration 10 --fps 60

import sys
import math
import argparse
import os
from pathlib import Path
import pygame as pg

try:
    import imageio
    _HAS_IMAGEIO = True
except Exception:
    _HAS_IMAGEIO = False

"""
Cow Enclosure — v13
- Interactif: plein écran par défaut (comme avant)
- Export vidéo: si --size donné → utilise WxH ; sinon → utilise résolution plein écran détectée
- Mode headless (pg.HIDDEN) pour export
- PNG OBLIGATOIRES à côté de la vidéo (dossier "<stem>_frames") — pas d'option pour désactiver
- NOUVEAU: --downscale k → rend EXACTEMENT la même animation mais exporte en W/k × H/k (ex: k=2 → moitié en pixels)
  ⚠️ L'animation, la mise en page, les proportions, etc., sont calculées à la résolution de base; seul l'export est redimensionné.
- NOUVEAU: --timescale s → accélère/ralentit uniformément la dynamique (s=2 → 2× plus vite; s=0.5 → 2× plus lent).
"""

FPS_DEFAULT = 60
TEXT_COLOR = (245, 245, 250)

# --- Fence style ---
POST_RADIUS    = 10
POST_OUTLINE   = 3
RAIL_WIDTH     = 8
RAIL_GAP       = 14
WOOD_FILL      = (245, 245, 245)
WOOD_DARK      = (200, 200, 200)
WOOD_LIGHT     = (255, 255, 255)

GRASS_FALLBACK = (46, 133, 64)

class Game:
    def __init__(self, width=None, height=None, fullscreen=True, hidden=False, timescale=1.0):
        pg.init()
        pg.font.init()

        flags = 0
        if fullscreen:
            flags |= pg.FULLSCREEN
        if hidden and hasattr(pg, "HIDDEN"):
            flags |= pg.HIDDEN

        if fullscreen:
            self.screen = pg.display.set_mode((0, 0), flags)
        else:
            if width is None or height is None:
                width, height = 1280, 720
            self.screen = pg.display.set_mode((width, height), flags)

        self.W, self.H = self.screen.get_size()
        self.clock = pg.time.Clock()
        self.timescale = float(timescale)
        try:
            self.font = pg.font.SysFont("menlo,consolas,monospace", 36, bold=True)
        except:
            self.font = pg.font.SysFont(None, 36)

        # Assets
        try:
            self.grass = pg.image.load("grass.png").convert()
        except:
            self.grass = None
        try:
            cow_src = pg.image.load("vache.png").convert_alpha()
        except Exception as e:
            print("Erreur: vache.png requis —", e)
            pg.quit(); sys.exit(1)

        # World (P fixed)
        self.P = 1100.0
        self.x_min = 16.0
        self.x_max = self.P/2.0 - self.x_min
        self.x = (self.x_min + self.x_max) / 2.0
        self.sweep_dir = 1
        self.sweep_speed = 52.
        self.margin_ratio = 0.08

        # Constant scale
        mw = int(self.W * self.margin_ratio)
        mh = int(self.H * self.margin_ratio)
        avail_w = self.W - 2*mw
        avail_h = self.H - 2*mh
        worst = self.P/2.0 - self.x_min
        self.scale = 0.94 * min(avail_w/worst, avail_h/worst)

        # Cow size + bobbing
        self.t = 0.0
        self.bob_freq = 0.12
        self.bob_amp  = 1.0
        target_w = max(64, min(220, int(min(self.W, self.H) * 0.10)))
        aspect = cow_src.get_height() / max(1, cow_src.get_width())
        target_h = max(64, min(220, int(target_w * aspect)))
        self.cow = pg.transform.smoothscale(cow_src, (target_w, target_h))

    def y_from_x(self, x):  # 2x+2y=P
        return max(self.x_min, self.P/2.0 - x)

    def draw_grass(self):
        if self.grass is None:
            self.screen.fill(GRASS_FALLBACK)
            return
        tw, th = self.grass.get_width(), self.grass.get_height()
        for y in range(0, self.H, th):
            for x in range(0, self.W, tw):
                self.screen.blit(self.grass, (x, y))

    def _rounded_segment(self, surf, p0, p1, width, color_fill, color_dark):
        x0, y0 = p0; x1, y1 = p1
        pg.draw.line(surf, color_fill, (x0, y0), (x1, y1), width)
        r = width // 2
        pg.draw.circle(surf, color_fill, (int(x0), int(y0)), r)
        pg.draw.circle(surf, color_fill, (int(x1), int(y1)), r)
        if width >= 6:
            pg.draw.line(surf, color_dark, (x0, y0), (x1, y1), 2)
            pg.draw.circle(surf, color_dark, (int(x0), int(y0)), r, 2)
            pg.draw.circle(surf, color_dark, (int(x1), int(y1)), r, 2)

    def draw_fence_rect(self, rx, ry, rw, rh):
        half = RAIL_WIDTH // 2
        gap  = RAIL_GAP

        y_top_outer1 = ry - (half + 0)
        y_top_outer2 = ry - (half + gap)
        y_bot_outer1 = ry + rh + (half + 0)
        y_bot_outer2 = ry + rh + (half + gap)

        self._rounded_segment(self.screen, (rx,      y_top_outer1), (rx+rw, y_top_outer1),
                          RAIL_WIDTH, WOOD_FILL, WOOD_DARK)
        self._rounded_segment(self.screen, (rx,      y_top_outer2), (rx+rw, y_top_outer2),
                          RAIL_WIDTH, WOOD_FILL, WOOD_DARK)
        self._rounded_segment(self.screen, (rx,      y_bot_outer1), (rx+rw, y_bot_outer1),
                          RAIL_WIDTH, WOOD_FILL, WOOD_DARK)
        self._rounded_segment(self.screen, (rx,      y_bot_outer2), (rx+rw, y_bot_outer2),
                          RAIL_WIDTH, WOOD_FILL, WOOD_DARK)

        x_left_outer1  = rx - (half + 0)
        x_left_outer2  = rx - (half + gap)
        x_right_outer1 = rx + rw + (half + 0)
        x_right_outer2 = rx + rw + (half + gap)

        self._rounded_segment(self.screen, (x_left_outer1,  ry), (x_left_outer1,  ry+rh),
                          RAIL_WIDTH, WOOD_FILL, WOOD_DARK)
        self._rounded_segment(self.screen, (x_left_outer2,  ry), (x_left_outer2,  ry+rh),
                          RAIL_WIDTH, WOOD_FILL, WOOD_DARK)
        self._rounded_segment(self.screen, (x_right_outer1, ry), (x_right_outer1, ry+rh),
                          RAIL_WIDTH, WOOD_FILL, WOOD_DARK)
        self._rounded_segment(self.screen, (x_right_outer2, ry), (x_right_outer2, ry+rh),
                          RAIL_WIDTH, WOOD_FILL, WOOD_DARK)

        TL = (rx - POST_RADIUS,        ry - POST_RADIUS)
        TR = (rx + rw + POST_RADIUS,   ry - POST_RADIUS)
        BR = (rx + rw + POST_RADIUS,   ry + rh + POST_RADIUS)
        BL = (rx - POST_RADIUS,        ry + rh + POST_RADIUS)

        for (cx, cy) in (TL, TR, BR, BL):
            pg.draw.circle(self.screen, WOOD_FILL, (cx, cy), POST_RADIUS)
            pg.draw.circle(self.screen, WOOD_DARK, (cx, cy), POST_RADIUS, POST_OUTLINE)
            pg.draw.circle(self.screen, WOOD_LIGHT, (cx-3, cy-3), max(2, POST_RADIUS//3))

    def draw_cow_centered(self, rx, ry, rw, rh, dt):
        self.t += dt * self.timescale
        bob = self.bob_amp * math.sin(2.0 * math.pi * self.bob_freq * self.t)
        img = self.cow
        cx = rx + rw//2 - img.get_width()//2
        cy = ry + rh//2 - img.get_height()//2 + int(bob)
        self.screen.blit(img, (cx, cy))

    def step(self, dt):
        self.x += self.sweep_dir * self.sweep_speed * dt * self.timescale
        y = self.y_from_x(self.x)
        Rmax = 3.
        ratio = max(self.x, y) / max(1e-6, min(self.x, y))
        if ratio > Rmax:
            if self.x > y:
                self.x = Rmax * y
            else:
                self.x = self.P/2.0 - (Rmax * self.x)
            self.sweep_dir *= -1
        if self.x >= self.x_max:
            self.x = self.x_max; self.sweep_dir = -1
        if self.x <= self.x_min:
            self.x = self.x_min; self.sweep_dir = +1

    def draw(self, dt):
        self.draw_grass()
        x = self.x
        y = self.y_from_x(x)
        rw = int(x * self.scale)
        rh = int(y * self.scale)
        rx = self.W//2 - rw//2
        ry = self.H//2 - rh//2

        self.draw_fence_rect(rx, ry, rw, rh)
        self.draw_cow_centered(rx, ry, rw, rh, dt)

        A = x * y / 100
        aire_label = self.font.render(f"A = {A:.1f}", True, TEXT_COLOR)
        self.screen.blit(aire_label, (int(self.W * 0.02), int(self.H * 0.3)))

        P = self.P / 10
        peri_label = self.font.render(f"P = {P:.1f}", True, TEXT_COLOR)
        self.screen.blit(peri_label, (int(self.W * 0.02), int(self.H * 0.3) + 50))

        pg.display.flip()

    def run(self, fps=FPS_DEFAULT):
        running = True
        while running:
            dt = self.clock.tick(fps) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key in (pg.K_ESCAPE, pg.K_q):
                        running = False
            self.step(dt)
            self.draw(dt)
        pg.quit()

    def export_video(self, filename, duration, fps=FPS_DEFAULT, downscale=1.0):
        """
        Exporte *toujours* les PNG à côté de la vidéo.
        - Dossier: <parent>/<stem>_frames
        - Fichiers: frame_00000.png, ...
        - Si imageio ne peut pas écrire, on garde quand même les PNG.
        - downscale>1.0 → exporte en résolution réduite (W/downscale, H/downscale) *sans changer* l'animation.
        """
        if downscale <= 0:
            raise ValueError("--downscale doit être > 0")

        nframes = int(duration * fps)

        # Prépare writer vidéo (si dispo)
        writer = None
        if _HAS_IMAGEIO:
            try:
                writer = imageio.get_writer(filename, fps=fps)
            except Exception as e:
                print("⚠️ imageio ne peut pas écrire la vidéo:", e)
                writer = None
        else:
            print("⚠️ imageio non disponible; export vidéo sauté (PNG seulement).")

        # Dossier PNG obligatoire: sibling du fichier vidéo
        out_path = Path(filename)
        png_path = out_path.parent / f"{out_path.stem}_frames"
        png_path.mkdir(parents=True, exist_ok=True)

        # Dimensions de sortie
        out_w = int(round(self.W / downscale))
        out_h = int(round(self.H / downscale))
        out_w = max(1, out_w)
        out_h = max(1, out_h)

        for i in range(nframes):
            dt = 1.0 / fps
            self.step(dt)
            self.draw(dt)

            # Crée une surface redimensionnée SANS toucher à la logique de rendu d'origine
            if downscale != 1.0:
                scaled_surf = pg.transform.smoothscale(self.screen, (out_w, out_h))
            else:
                scaled_surf = self.screen

            # vidéo (si possible)
            if writer is not None:
                frame_rgb = pg.surfarray.array3d(scaled_surf).swapaxes(0, 1)
                writer.append_data(frame_rgb)

            # png
            out = png_path / f"frame_{i:05d}.png"
            # pg.image.save exige une Surface; on sauve la surface redimensionnée
            pg.image.save(scaled_surf, str(out))

        if writer is not None:
            writer.close()
            print(f"✅ Export vidéo: {filename} ({nframes} frames @ {fps} fps)")
        print(f"✅ PNG sauvegardés dans: {png_path} ({nframes} images)")

def parse_args():
    p = argparse.ArgumentParser(description="Cow Enclosure animation (interactive & export)")
    p.add_argument("--export", metavar="FICHIER", help="Si fourni: exporte la vidéo dans ce fichier (ex: output.mp4) + PNG à côté")
    p.add_argument("--duration", type=float, default=10.0, help="Durée de la vidéo à exporter (secondes)")
    p.add_argument("--fps", type=int, default=FPS_DEFAULT, help="Images/seconde pour l'export")
    p.add_argument("--size", metavar="WxH", help="Résolution fixe (ex: 1080x1920). Si omis → utilise la résolution fullscreen détectée")
    p.add_argument("--downscale", type=float, default=1.0, help="Facteur de réduction à l'export (ex: 2 → moitié en pixels; 1 → identique)")
    p.add_argument("--timescale", type=float, default=1.0, help="Accélère/ralentit toute l'animation (ex: 2 → 2x plus vite; 0.5 → deux fois plus lent)")
    p.add_argument("--no-fullscreen", action="store_true", help="Fenêtré en mode interactif")
    return p.parse_args()

def parse_size(s):
    try:
        w, h = s.lower().split("x")
        return int(w), int(h)
    except Exception:
        raise SystemExit("Taille invalide pour --size. Exemple: 1280x720")

if __name__ == "__main__":
    args = parse_args()

    if args.export:
        if args.size:
            W, H = parse_size(args.size)
            g = Game(width=W, height=H, fullscreen=False, hidden=True, timescale=args.timescale)
        else:
            # Plein écran caché → reprend la résolution native de l'écran
            g = Game(fullscreen=True, hidden=True, timescale=args.timescale)
        try:
            g.export_video(args.export, args.duration, fps=args.fps, downscale=args.downscale)
        except Exception as e:
            print("Error during export:", e)
        finally:
            pg.quit(); sys.exit(0)
    else:
        fullscreen = not args.no_fullscreen
        g = Game(fullscreen=fullscreen, timescale=args.timescale)
        try:
            g.run(fps=args.fps)
        except Exception as e:
            print("Error:", e)
            pg.quit(); sys.exit(1)
