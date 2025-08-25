import pygame, sys, math, random, os, subprocess
from pygame import gfxdraw

# ================== Config export ==================
W, H = 960, 440
FPS = 60
EXPORT_DIR = "exports/train_lightclock"
os.makedirs(EXPORT_DIR, exist_ok=True)

# ================== Couleurs ==================
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 214, 10)
STEEL_D   = (70, 70, 78)
STEEL_L   = (110, 110, 120)
BODY      = (38, 44, 68)
ACCENT    = (220, 80, 60)
WINDOW    = (20, 28, 40)
SMOKE_COL = (210, 210, 210)

# ================== Dimensions ==================
LOCO_W, LOCO_H = 90, 90
WAG_W,  WAG_H  = 180, 150
GAP = 12  # attelage

# ================== Paramètres anim ==================
Y_BODY_OFFSET = 50
R_WAG  = 20
R_MAIN = 24
RAIL_Y = H - 110

ROLL_DIR    = +1           # sens de rotation roues
TRAIN_SPEED = 120.0        # px/s
HALF_PERIOD = 0.8          # s (bas->haut OU haut->bas du photon)

# ---- Timing exact demandé ----
START_OVERLAP = 10                   # la loco dépasse à gauche au premier frame
ROUNDS = 3                           # nb d’allers-retours du photon
T_END  = ROUNDS * (3.34 * HALF_PERIOD)

# ---- Trajectoire pointillée (jaune) ----
DASH_LEN   = 6
SKIP_LEN   = 2
LINE_WIDTH = 1
YELLOW_A   = (255, 214, 10, 220)     # jaune avec alpha

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Train + Horloge lumineuse (export)")
clock = pygame.time.Clock()

# Surface alpha pour les pointillés
trail_surf = pygame.Surface((W, H), pygame.SRCALPHA)

# ================== Rails ==================
def draw_rails(surface, y_line):
    pygame.draw.line(surface, (200,200,200), (0, y_line), (W, y_line), 2)

# ================== Train (joli) ==================
def draw_cartoon_train(surface, x_center_loco, rail_y, wheel_angle):
    y_body = rail_y - Y_BODY_OFFSET
    loco_rect  = pygame.Rect(x_center_loco - LOCO_W, y_body - LOCO_H, LOCO_W, LOCO_H)
    wagon_rect = pygame.Rect(loco_rect.left - GAP - WAG_W, y_body - WAG_H + 8, WAG_W, WAG_H)

    # --- WAGON ---
    pygame.draw.rect(surface, BODY, wagon_rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, wagon_rect, 2, border_radius=8)
    band = pygame.Rect(wagon_rect.x, wagon_rect.bottom - 16, WAG_W, 12)
    pygame.draw.rect(surface, ACCENT, band, border_radius=6)
    win_w, win_h, pad = 46, 32, 12
    for i in range(3):
        r = pygame.Rect(wagon_rect.x + pad + i * (win_w + pad), wagon_rect.y + 14, win_w, win_h)
        pygame.draw.rect(surface, WINDOW, r, border_radius=6)
        pygame.draw.rect(surface, STEEL_L, r, 2, border_radius=6)
        refl = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        pygame.draw.polygon(refl, (255,255,255,40), [(0,5),(r.width*0.6,0),(r.width*0.6,6),(0,11)])
        pygame.draw.polygon(refl, (255,255,255,25), [(r.width*0.7,r.height-10),(r.width,r.height-16),(r.width,r.height-12),(r.width*0.7,r.height-6)])
        surface.blit(refl, (r.x, r.y))

    # Attelage
    cy = wagon_rect.bottom - 10
    pygame.draw.line(surface, STEEL_L, (wagon_rect.right, cy), (loco_rect.left, cy), 3)

    # --- LOCO ---
    pygame.draw.rect(surface, BODY, loco_rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, loco_rect, 2, border_radius=10)
    # Cabine + gloss
    cab = pygame.Rect(loco_rect.x + 10, loco_rect.y + 10, 36, 36)
    pygame.draw.rect(surface, WINDOW, cab, border_radius=6)
    pygame.draw.rect(surface, STEEL_L, cab, 2, border_radius=6)
    glass = pygame.Surface((cab.width, cab.height), pygame.SRCALPHA)
    pygame.draw.polygon(glass, (255,255,255,40), [(0,4),(cab.width*0.6,0),(cab.width*0.6,6),(0,10)])
    surface.blit(glass, (cab.x, cab.y))
    # Nez arrondi
    nose_rect = pygame.Rect(loco_rect.right - 26, loco_rect.y + 18, 22, 26)
    pygame.draw.ellipse(surface, BODY, nose_rect); pygame.draw.ellipse(surface, WHITE, nose_rect, 2)
    # Cheminée
    chim = pygame.Rect(loco_rect.right - 32, loco_rect.y - 18, 18, 20)
    pygame.draw.rect(surface, STEEL_D, chim, border_radius=4); pygame.draw.rect(surface, WHITE, chim, 2, border_radius=4)
    # Liseré déco
    deco = pygame.Rect(loco_rect.x + 6, loco_rect.bottom - 16, LOCO_W - 12, 8)
    pygame.draw.rect(surface, ACCENT, deco, border_radius=4)
    # Gloss / shade caisse
    gloss = pygame.Surface((loco_rect.width, loco_rect.height), pygame.SRCALPHA)
    pygame.draw.polygon(gloss, (255,255,255,26), [(0,10),(loco_rect.width*0.7,0),(loco_rect.width*0.7,8),(0,18)])
    shade = pygame.Surface((loco_rect.width, loco_rect.height), pygame.SRCALPHA)
    for yy in range(loco_rect.height):
        alpha = int(40 * (yy/loco_rect.height))
        pygame.draw.line(shade, (0,0,0,alpha), (0,yy), (loco_rect.width,yy))
    gloss.blit(shade,(0,0))
    surface.blit(gloss, (loco_rect.x, loco_rect.y))

    # --- Roues + bielle ---
    wheel_y_wag  = rail_y - R_WAG
    wheel_y_loco = rail_y - R_MAIN

    def nice_wheel(cx, cy, r):
        gfxdraw.filled_circle(surface, cx, cy, r, STEEL_D)
        gfxdraw.aacircle(surface, cx, cy, r, WHITE)
        gfxdraw.filled_circle(surface, cx, cy, max(1, r-4), BODY)
        gfxdraw.aacircle(surface, cx, cy, max(1, r-4), STEEL_L)
        gfxdraw.filled_circle(surface, cx, cy, max(4, r//3), STEEL_L)
        for a in range(0, 360, 60):
            ax = cx + int((r-6) * math.cos(math.radians(a + wheel_angle)))
            ay = cy + int((r-6) * math.sin(math.radians(a + wheel_angle)))
            pygame.draw.line(surface, STEEL_L, (cx, cy), (ax, ay), 2)

    for cx in (wagon_rect.x + 40, wagon_rect.centerx, wagon_rect.right - 40):
        nice_wheel(cx, wheel_y_wag, R_WAG)

    cx_main = loco_rect.centerx - 14
    nice_wheel(cx_main, wheel_y_loco, R_MAIN)

    pin_x = int(cx_main + R_MAIN * 0.95 * math.cos(math.radians(wheel_angle)))
    pin_y = int(wheel_y_loco + R_MAIN * 0.95 * math.sin(math.radians(wheel_angle)))
    gfxdraw.filled_circle(surface, pin_x, pin_y, 3, ACCENT)

    piston_y = wheel_y_loco - 10
    piston_x = loco_rect.x + 6
    pygame.draw.line(surface, STEEL_L, (pin_x, pin_y), (piston_x, piston_y), 3)
    piston = pygame.Rect(piston_x - 6, piston_y - 6, 18, 12)
    pygame.draw.rect(surface, STEEL_D, piston, border_radius=3); pygame.draw.rect(surface, WHITE, piston, 1, border_radius=3)

    # Ombre
    shadow_w = (wagon_rect.width + GAP + LOCO_W)
    shadow = pygame.Surface((shadow_w, 20), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0,0,0,80), shadow.get_rect())
    surface.blit(shadow, (wagon_rect.x, rail_y - 18))

    emitter = (chim.centerx, chim.top)
    return wagon_rect, emitter

# ================== Horloge lumineuse ==================
def draw_light_clock_outside(surface, wagon_rect, t, half_period):
    top_y = wagon_rect.y + 44
    bot_y = wagon_rect.bottom - 44
    x_c   = wagon_rect.centerx

    # Miroirs
    pygame.draw.line(surface, WHITE, (x_c - 25, top_y), (x_c + 25, top_y), 2)
    pygame.draw.line(surface, WHITE, (x_c - 25, bot_y), (x_c + 25, bot_y), 2)

    # Mouvement triangulaire (bas -> haut -> bas)
    period = 2.0 * half_period
    u = (t % period) / period
    s = 2*u if u < 0.5 else 2*(1 - u)
    y = bot_y + (top_y - bot_y) * s

    px, py = int(x_c), int(y)
    pygame.draw.circle(surface, YELLOW, (px, py), 4)
    return px, py

# ================== Fumée simple ==================
class Smoke:
    __slots__ = ("x","y","vx","vy","r","a")
    def __init__(self, x, y):
        self.x, self.y = x + random.uniform(-2,2), y + random.uniform(-2,2)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-100, -60)
        self.r  = 5.0
        self.a  = 200.0
    def step(self, dt):
        self.vx += -15.0 * dt
        self.vy += -20.0 * dt
        self.x  += self.vx * dt
        self.y  += self.vy * dt
        self.r  += 16.0 * dt
        self.a  -= 90.0 * dt
        return self.a > 0 and self.r < 60
    def draw(self, surf):
        rr1 = max(1, int(self.r))
        a1 = max(0, min(255, int(self.a)))
        gfxdraw.filled_circle(surf, int(self.x), int(self.y), rr1, (SMOKE_COL[0],SMOKE_COL[1],SMOKE_COL[2], a1))
        gfxdraw.aacircle(surf,  int(self.x), int(self.y), rr1, (230,230,230))

# ================== Util : polyligne pointillée ==================
def draw_dashed_polyline(surface, points, color, width=2, dash_len=12, skip_len=8):
    if len(points) < 2:
        return
    step = dash_len + skip_len
    total = 0.0
    for i in range(len(points)-1):
        (x1, y1), (x2, y2) = points[i], points[i+1]
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            continue
        vx, vy = dx / dist, dy / dist
        offset = (-total) % step
        s = offset
        while s < dist:
            sx = x1 + vx * s
            sy = y1 + vy * s
            ex = x1 + vx * min(s + dash_len, dist)
            ey = y1 + vy * min(s + dash_len, dist)
            pygame.draw.line(surface, color, (sx, sy), (ex, ey), width)
            s += step
        total += dist

# ================== Boucle export ==================
clock = pygame.time.Clock()
trail = []
smokes = []

# Départ : loco visible (mord le bord gauche)
train_x = LOCO_W - START_OVERLAP
wheel_angle = 0.0
t = 0.0
frame_id = 0

while True:
    dt = 1.0 / FPS
    t  += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    wheel_angle = (wheel_angle + ROLL_DIR * 180 * dt) % 360
    train_x    += TRAIN_SPEED * dt

    screen.fill(BLACK)
    draw_rails(screen, RAIL_Y)

    loco_center_x = int(train_x)
    wagon_rect, emitter = draw_cartoon_train(screen, loco_center_x, RAIL_Y, wheel_angle)
    px, py = draw_light_clock_outside(screen, wagon_rect, t, HALF_PERIOD)

    # Fumée
    if random.random() < 6 * dt:
        smokes.append(Smoke(emitter[0], emitter[1]))
    smokes = [s for s in smokes if s.step(dt)]
    for s in smokes:
        s.draw(screen)

    # Trajectoire pointillée (jaune) — redessin propre à chaque frame
    trail.append((px, py))
    # trail = trail[-900:]  # (optionnel) limiter longueur pour effet « comète »
    trail_surf.fill((0,0,0,0))
    draw_dashed_polyline(trail_surf, trail, YELLOW_A, width=LINE_WIDTH, dash_len=DASH_LEN, skip_len=SKIP_LEN)
    screen.blit(trail_surf, (0,0))

    # Sauvegarde PNG
    pygame.image.save(screen, os.path.join(EXPORT_DIR, f"frame_{frame_id:04d}.png"))
    frame_id += 1

    pygame.display.flip()
    clock.tick(FPS)

    # Stop net après 3 allers-retours du photon
    if t >= T_END:
        pygame.quit()
        mp4_path = os.path.join(EXPORT_DIR, "train_lightclock.mp4")
        subprocess.run([
            "ffmpeg","-y","-framerate", str(FPS),
            "-i", os.path.join(EXPORT_DIR, "frame_%04d.png"),
            "-c:v","libx264","-pix_fmt","yuv420p","-crf","18", mp4_path
        ])
        print("Export fini :", mp4_path)
        sys.exit(0)
