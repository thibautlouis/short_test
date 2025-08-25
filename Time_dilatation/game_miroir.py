import pygame, sys, os, subprocess

# ==== EXPORT CONFIG ====
EXPORT_DIR = "exports/clock_simple_td"
os.makedirs(EXPORT_DIR, exist_ok=True)
EXPORT_FRAMES = True
FRAME_ID = 0
FPS = 60

# ==== SCÈNE ====
W, H = 600, 600
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 214, 10)

# miroirs / balle
HALF_PERIOD = 0.78         # s (bas->haut ou haut->bas)
DURATION    = 3.0         # durée cible; on allonge juste assez pour finir en bas
TOP_Y       = 120
BOT_Y       = H - 120
LINE_THICK  = 6
BALL_R      = 10

pygame.init()
screen = pygame.display.set_mode((W, H))

# --- Police "type Manim" (Latin Modern / Computer Modern) ---
def get_manim_like_font(size=32, italic=True):
    # Noms de polices proches de la police LaTeX par défaut
    candidates = [
        "Latin Modern Roman",
        "Latin Modern Math",
        "Latin Modern",
        "CMU Serif",
        "Computer Modern",
        "STIX Two Text",
        "STIXGeneral",
        "TeX Gyre Termes",
        "TeX Gyre Pagella",
    ]
    path = None
    for name in candidates:
        path = pygame.font.match_font(name)
        if path:
            break
    if path:
        f = pygame.font.Font(path, size)
        f.set_italic(italic)   # rendu façon math (italique)
        return f
    # fallback propre si aucune police “LM/CM” n’est trouvée
    return pygame.font.SysFont(None, size, italic=italic)

font_manim = get_manim_like_font(32, italic=True)

def tri01(t, period):
    u = (t % period) / period
    return 2*u if u < 0.5 else 2*(1 - u)

def draw_light_clock(surface, t, half_period):
    x_c = W // 2
    # miroirs
    pygame.draw.line(surface, WHITE, (x_c - 80, TOP_Y), (x_c + 80, TOP_Y), LINE_THICK)
    pygame.draw.line(surface, WHITE, (x_c - 80, BOT_Y), (x_c + 80, BOT_Y), LINE_THICK)
    # bornes sûres (centre ne dépasse pas)
    half_line = LINE_THICK / 2
    y_high = TOP_Y + BALL_R + half_line
    y_low  = BOT_Y - BALL_R - half_line
    # mouvement triangulaire
    period = 2.0 * half_period
    s = tri01(t, period)
    y = y_low + (y_high - y_low) * s
    pygame.draw.circle(surface, YELLOW, (x_c, int(round(y))), BALL_R)

def aligned_end(duration, half_period):
    period = 2.0 * half_period   # bas->haut->bas
    extra = (period - (duration % period)) % period
    return duration + extra

def draw_double_arrow(surface, x, y1, y2, color=WHITE, width=2, head=10, text=None, font=None):
    """Dessine une double flèche verticale entre y1 et y2 à l'abscisse x."""
    # ligne centrale
    pygame.draw.line(surface, color, (x, y1), (x, y2), width)
    # flèche en haut
    pygame.draw.line(surface, color, (x, y1), (x-head, y1+head), width)
    pygame.draw.line(surface, color, (x, y1), (x+head, y1+head), width)
    # flèche en bas
    pygame.draw.line(surface, color, (x, y2), (x-head, y2-head), width)
    pygame.draw.line(surface, color, (x, y2), (x+head, y2-head), width)

    if text and font:
        label = font.render(text, True, color)
        mid_y = (y1 + y2) // 2 - label.get_height() // 2
        # un peu à gauche de la flèche
        surface.blit(label, (x - 24 - label.get_width(), mid_y))

# ========= main export loop =========
clock = pygame.time.Clock()
t = 0.0
t_end = aligned_end(DURATION, HALF_PERIOD)
running = True

while running:
    dt = 1.0 / FPS
    t += dt
    screen.fill(BLACK)
    draw_light_clock(screen, t, HALF_PERIOD)

    # --- Affichage de la double flèche L à gauche ---
    L = BOT_Y - TOP_Y  # distance entre les miroirs (en px)
    draw_double_arrow(screen, 80, TOP_Y, BOT_Y, WHITE, width=2, head=12, text="L", font=font_manim)

    if EXPORT_FRAMES:
        pygame.image.save(screen, os.path.join(EXPORT_DIR, f"frame_{FRAME_ID:04d}.png"))
        FRAME_ID += 1

    pygame.display.flip()
    clock.tick(FPS)

    if t >= t_end:
        running = False

pygame.quit()

# ====== assemble MP4 via ffmpeg ======
if EXPORT_FRAMES:
    mp4_path = os.path.join(EXPORT_DIR, "clock_simple_td.mp4")
    subprocess.run([
        "ffmpeg","-y","-framerate", str(FPS),
        "-i", os.path.join(EXPORT_DIR, "frame_%04d.png"),
        "-c:v","libx264","-pix_fmt","yuv420p","-crf","18", mp4_path
    ])
    print("Export fini :", mp4_path)
