# ffmpeg -y -i doppler_static.mp4  -i son_ambulance.wav -t 8.30   -c:v copy -af  "volume=0.8" -c:a aac -shortest doppler_static_audio.mp4

import os
import math
import pygame
from pygame import gfxdraw

# =====================
# Assets
# =====================
ASSET_BG = os.path.join(os.path.dirname(__file__), "fond_route.png")
ASSET_CAR_A = os.path.join(os.path.dirname(__file__), "sprite_voiture.png")
ASSET_CAR_B = os.path.join(os.path.dirname(__file__), "sprite_voiture2.png")
ASSET_OBS   = os.path.join(os.path.dirname(__file__), "obs.png")  # sprite observateur

# =====================
# Window & presets
# =====================
WINDOW_SCALE = 0.8
FPS = 60

# =====================
# Road geometry
# =====================
ROAD_HEIGHT_F = 0.26
ROAD_CENTER_F = 0.50

# =====================
# Doppler parameters
# =====================
WAVE_SPEED = 140.0      # expansion (px/s)
EMIT_HZ = 1.           # fréquence **constante** (ondes/s)
WAVE_MAX_AGE = 6.0      # durée de vie (s)

# =====================
# Car controls
# =====================
CAR_POS_MODE = "manual"   # "auto" ou "manual" -> ici statique et visible
CAR_X = 200               # ignoré, on positionne en relatif à W plus bas
CAR_Y_ON_ROAD = 0.35      # 0=haut route, 1=bas route
CAR_WIDTH_F = 0.12        # fraction largeur fenêtre
LIGHTS_HZ = 1.0           # clignotement gyro
LIGHTS_START_DELAY = 0.5  # délai avant clignotement

# Mouvement AUTO (inactif si "manual")
AUTO_SPEED_PX = 120.0
AUTO_START_X_F = 1.08
AUTO_END_X_F   = -0.08
AUTO_IDLE_S    = 0.8
AUTO_LOOP      = False

# Offset du gyro sur le sprite
GYRO_OFFSET_Y_F = 0
GYRO_OFFSET_X_F = -0.  # fraction de la longueur du sprite (ajuste si besoin)

# =====================
# Colors
# =====================
WHITE = (242, 242, 245)
BLUE  = ( 60, 130, 255)

# =====================
# Recording (export)
# =====================
RECORD_PNG = True           # export PNG frames
RECORD_MP4 = True           # build MP4 à la fin
RECORD_FPS = 15             # <-- tu peux ajuster pour un rendu plus lent
RECORD_DIR = os.path.join(os.path.dirname(__file__), "export_frames_static")
RECORD_MP4_PATH = os.path.join(os.path.dirname(__file__), "doppler_static.mp4")
AUDIO_WAV_PATH = os.path.join(os.path.dirname(__file__), "son_ambulance.wav")
RECORD_AUDIO_TO_MP4 = True  # tente de muxer l'audio WAV dans le MP4 via ffmpeg

# Durée d'export (on stoppe après ce temps)
RUN_DURATION_S = 15.0


# =====================
# Utils
# =====================
def draw_ring_alpha(surface, x, y, r, base_color, alpha, width=3, ssaa=2):
    if r <= 0 or alpha <= 0:
        return
    R, G, B = base_color
    rad = int(max(1, round(r)))
    w = max(1, int(width))
    a_bucket = max(0, min(64, int(64 * alpha)))
    key = (rad, w, a_bucket, ssaa)

    if not hasattr(draw_ring_alpha, "_cache"):
        draw_ring_alpha._cache = {}
    cache = draw_ring_alpha._cache

    surf = cache.get(key)
    if surf is None:
        A = int(255 * (a_bucket / 64))
        pad = w + 2
        size = 2 * (rad + pad) + 1
        big_size = size * ssaa
        big = pygame.Surface((big_size, big_size), pygame.SRCALPHA)
        cx = cy = big_size // 2
        big_rad = rad * ssaa
        big_w = w * ssaa

        pygame.draw.circle(big, (R, G, B, A), (cx, cy), big_rad, big_w)
        gfxdraw.aacircle(big, cx, cy, big_rad, (R, G, B, A))
        if big_rad - big_w > 0:
            gfxdraw.aacircle(big, cx, cy, big_rad - big_w, (R, G, B, A))

        surf = pygame.transform.smoothscale(big, (size, size))
        if len(cache) > 512:
            cache.clear()
        cache[key] = surf

    surface.blit(surf, (int(x) - surf.get_width() // 2,
                        int(y) - surf.get_height() // 2))

# =====================
# Main
# =====================

def main():
    pygame.init()
    pygame.display.set_caption("Effet Doppler — voiture de police statique (export)")

    # --- Son (sirène) ---
    siren = None
    try:
        pygame.mixer.init()
        siren = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "son_ambulance.wav"))
        siren.play(loops=-1)
    except Exception as e:
        print("Impossible de jouer le son:", e)

    # Fond → fenêtre → convert
    bg_raw = pygame.image.load(ASSET_BG)
    bg_w, bg_h = bg_raw.get_width(), bg_raw.get_height()
    W, H = int(bg_w * WINDOW_SCALE), int(bg_h * WINDOW_SCALE)
    screen = pygame.display.set_mode((W, H))
    background = pygame.transform.smoothscale(bg_raw.convert(), (W, H))

    # Sprites voiture → **même taille exactement**
    car_a_src = pygame.image.load(ASSET_CAR_A).convert_alpha()
    car_b_src = pygame.image.load(ASSET_CAR_B).convert_alpha()
    target_w = max(20, int(W * CAR_WIDTH_F))
    ref_h = int(car_a_src.get_height() * target_w / car_a_src.get_width())
    target_size = (target_w, ref_h)
    car_a = pygame.transform.smoothscale(car_a_src, target_size)
    car_b = pygame.transform.smoothscale(car_b_src, target_size)

    # Sprite observateur (mise à l'échelle relative à la fenêtre)
    obs_src = pygame.image.load(ASSET_OBS).convert_alpha()
    obs_w = int(W * 0.03)
    obs_h = int(obs_src.get_height() * obs_w / obs_src.get_width())
    observer_sprite = pygame.transform.smoothscale(obs_src, (obs_w, obs_h))

    clock = pygame.time.Clock()

    # Route
    road_h = int(H * ROAD_HEIGHT_F)
    road_y_center = int(H * ROAD_CENTER_F)
    road_top = road_y_center - road_h // 2
    road_bottom = road_y_center + road_h // 2

    def road_y_from_fraction(frac):
        frac = max(0.0, min(1.0, frac))
        return int(road_top + frac * (road_bottom - road_top))

    # Observateur
    observer_pos = (W // 2, int(H * 0.66))

    # Horloges
    t_motion = 0.0
    paused = False
    slowmo = False
    t_start = pygame.time.get_ticks() / 1000.0

    # Émission **par horloge fixe**
    period = 1.0 / EMIT_HZ
    now = t_start
    next_emit_time = now  # première onde possible immédiatement quand visible

    wavefronts = []

    # "manual" statique
    auto_state = "idle"
    auto_tstate = 0.0
    x_car = 0

    # Init enregistrement
    if RECORD_PNG or RECORD_MP4:
        os.makedirs(RECORD_DIR, exist_ok=True)
        # Nettoie anciens PNG
        for _f in os.listdir(RECORD_DIR):
            if _f.lower().endswith(".png"):
                try:
                    os.remove(os.path.join(RECORD_DIR, _f))
                except Exception:
                    pass
    frame_idx = 0

    running = True
    try:
        while running:
            dt_real = clock.tick(FPS) / 1000.0
            now = pygame.time.get_ticks() / 1000.0

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False
                    elif e.key == pygame.K_SPACE:
                        paused = not paused
                    elif e.key == pygame.K_s:
                        slowmo = not slowmo

            if not paused:
                dt_motion = dt_real * (0.25 if slowmo else 1.0)
                t_motion += dt_motion
                auto_tstate += dt_motion
            else:
                dt_motion = 0.0

            # Position Y (statique)
            y_car = road_y_from_fraction(CAR_Y_ON_ROAD)

            # Position X statique et visible (70% de la largeur)
            x_car = int(0.70 * W)

            car_pos = (x_car, y_car)

            # Visibilité de la voiture à l'écran (utilise la taille de car_a)
            screen_rect = pygame.Rect(0, 0, W, H)
            car_rect_for_vis = car_a.get_rect(center=car_pos)
            car_visible = car_rect_for_vis.colliderect(screen_rect)

            # ÉMISSIONS À HORLOGE FIXE (seulement si la voiture est visible)
            if car_visible:
                while now >= next_emit_time:
                    car_ref = car_a
                    gyro_y = car_pos[1] + int(GYRO_OFFSET_Y_F * car_ref.get_height())
                    gyro_x = car_pos[0] + int(GYRO_OFFSET_X_F * car_ref.get_width())

                    wavefronts.append({"x": float(gyro_x),
                                       "y": float(gyro_y),
                                       "age": 0.0})
                    next_emit_time += period
            else:
                # évite les paquets d'ondes dès l'entrée à l'écran
                next_emit_time = now

            # Mise à jour ondes (temps réel)
            alive = []
            for wf in wavefronts:
                wf["age"] += dt_real
                if wf["age"] < WAVE_MAX_AGE:
                    alive.append(wf)
            wavefronts = alive[-80:]

            # Stop après RUN_DURATION_S
            if (now - t_start) >= RUN_DURATION_S:
                running = False

            # ---------- Rendu ----------
            screen.blit(background, (0, 0))

            # Observateur
            obs_rect = observer_sprite.get_rect(center=observer_pos)
            screen.blit(observer_sprite, obs_rect)

            # Voiture (gyro clignotant)
            if t_motion >= LIGHTS_START_DELAY:
                phase = math.sin(2 * math.pi * LIGHTS_HZ * (t_motion - LIGHTS_START_DELAY))
                car_surf = car_a if phase >= 0 else car_b
            else:
                car_surf = car_a
            rect = car_surf.get_rect(center=car_pos)
            screen.blit(car_surf, rect)

            # Ondes
            for wf in wavefronts:
                r = WAVE_SPEED * wf["age"]
                fade_age  = max(0.0, 1.0 - wf["age"] / WAVE_MAX_AGE)
                fade_dist = max(0.0, 1.0 - r / (0.6 * W))
                fade = (fade_age * fade_dist) ** 0.5
                if fade <= 0.05:
                    continue
                if (wf["x"] + r < -50) or (wf["x"] - r > W + 50) or (wf["y"] + r < -50) or (wf["y"] - r > H + 50):
                    continue
                draw_ring_alpha(screen, wf["x"], wf["y"], r, BLUE, fade, width=3)

            pygame.display.flip()

            # --- Export frame ---
            if RECORD_PNG or RECORD_MP4:
                out_path = os.path.join(RECORD_DIR, f"frame_{frame_idx:05d}.png")
                try:
                    pygame.image.save(screen, out_path)
                    frame_idx += 1
                except Exception as ex:
                    print("Erreur export frame:", ex)
    finally:
        # Arrêt audio + pygame
        try:
            pygame.mixer.stop()
        except Exception:
            pass
        try:
            pygame.mixer.quit()
        except Exception:
            pass
        pygame.quit()

        # --- Build MP4 from PNG frames ---
        if (RECORD_PNG or RECORD_MP4) and RECORD_MP4:
            try:
                import imageio.v2 as imageio
                frames = sorted([f for f in os.listdir(RECORD_DIR) if f.lower().endswith(".png")])
                if frames:
                    with imageio.get_writer(RECORD_MP4_PATH, fps=RECORD_FPS, codec='libx264', quality=8) as writer:
                        for fname in frames:
                            writer.append_data(imageio.imread(os.path.join(RECORD_DIR, fname)))
                print(f"MP4 écrit : {RECORD_MP4_PATH} ({len(frames)} frames)")
            except Exception as e:
                print("MP4 non généré (imageio/libx264 manquant ?). PNG disponibles dans:", RECORD_DIR)

if __name__ == "__main__":
    main()
