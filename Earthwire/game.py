# export_rope_seq_fade.py
# Exporte frames PNG : earth_fade/, earth_only/, rope_draw/, rope_grow/

import pygame, sys, math, os

W, H = 540, 960
FPS = 60

EARTH_PATH = "earth_cut.png"
ROPE_PATH  = "rope_cut.png"

DUR_EARTH_FADE = 1.2
DUR_EARTH_ONLY = 0.8
DUR_ROPE_DRAW  = 1.2
DUR_ROPE_GROW  = 1.2

ROPE_GROW_FACTOR = 1.02
EARTH_SCALE_W = 0.80
EARTH_ZOOM_START = 0.88
BASE_ROPE_SCALE = 1.05
CENTER = (W//2, H//2)

def ease_out_cubic(t): return 1 - (1 - t) ** 3
def clamp(x,a,b): return max(a, min(b, x))

def sector_mask(size, theta, start_angle=-math.pi/2):
    w, h = size
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w/2, h/2
    R = max(w, h)*0.6
    steps = max(8, int(120 * theta / (2*math.pi)))
    pts = [(cx, cy)]
    for i in range(steps+1):
        ang = start_angle + (theta * i/max(1,steps))
        pts.append((cx + R*math.cos(ang), cy + R*math.sin(ang)))
    pygame.draw.polygon(surf, (255,255,255,255), pts)
    return surf

def blit_with_sector(canvas, image, center, theta):
    mask = sector_mask(image.get_size(), theta)
    tmp = image.copy()
    tmp.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    rect = tmp.get_rect(center=center)
    canvas.blit(tmp, rect)

def ensure_dir(path): os.makedirs(path, exist_ok=True)

def prep_assets():
    pygame.display.set_mode((1,1))  # nécessaire pour convert_alpha
    earth_raw = pygame.image.load(EARTH_PATH).convert_alpha()
    rope_raw  = pygame.image.load(ROPE_PATH).convert_alpha()
    earth_target_w = int(W * EARTH_SCALE_W)
    ratio = earth_raw.get_height() / earth_raw.get_width()
    earth_final = pygame.transform.smoothscale(earth_raw, (earth_target_w, int(earth_target_w*ratio)))
    earth_rect = earth_final.get_rect(center=CENTER)
    return earth_final, earth_rect, rope_raw

def rope_for_factor(rope_raw, earth_rect, factor):
    target_w = int(earth_rect.width * BASE_ROPE_SCALE * factor)
    r = rope_raw.get_height()/rope_raw.get_width()
    rope = pygame.transform.smoothscale(rope_raw, (target_w, int(target_w*r)))
    rect = rope.get_rect(center=(CENTER[0]-1, CENTER[1]))
    return rope, rect

def export_sequence(name, frames, draw_fn):
    ensure_dir(f"exports/{name}")
    for i in range(frames):
        t = (i+1)/frames
        surf = pygame.Surface((W,H), pygame.SRCALPHA)
        draw_fn(surf, t)
        pygame.image.save(surf, f"exports/{name}/frame_{i:05d}.png")
    print(f"[OK] exports/{name}: {frames} frames")

def main():
    pygame.init()
    earth_final, earth_rect, rope_raw = prep_assets()

    # 1) fade+zoom Terre
    f1 = int(DUR_EARTH_FADE*FPS)
    def draw_fade(surf,t):
        surf.fill((0,0,0))
        s = EARTH_ZOOM_START + (1.0-EARTH_ZOOM_START)*ease_out_cubic(t)
        w = int(earth_final.get_width()*s)
        h = int(earth_final.get_height()*s)
        e = pygame.transform.smoothscale(earth_final,(w,h))
        e.set_alpha(int(255*t))
        rect = e.get_rect(center=CENTER)
        surf.blit(e, rect)
    export_sequence("earth_fade", f1, draw_fade)

    # 2) Terre seule
    f2 = int(DUR_EARTH_ONLY*FPS)
    def draw_only(surf,t):
        surf.fill((0,0,0))
        surf.blit(earth_final, earth_rect)
    export_sequence("earth_only", f2, draw_only)

    # 3) corde qui se dessine
    f3 = int(DUR_ROPE_DRAW*FPS)
    def draw_draw(surf,t):
        surf.fill((0,0,0))
        surf.blit(earth_final, earth_rect)
        theta = 2*math.pi*ease_out_cubic(t)
        rope_img,_ = rope_for_factor(rope_raw, earth_rect, 1.0)
        blit_with_sector(surf, rope_img, (CENTER[0]-1,CENTER[1]), theta)
    export_sequence("rope_draw", f3, draw_draw)

    # 4) corde qui grandit
    f4 = int(DUR_ROPE_GROW*FPS)
    def draw_grow(surf,t):
        surf.fill((0,0,0))
        surf.blit(earth_final, earth_rect)
        f = 1.0+(ROPE_GROW_FACTOR-1.0)*ease_out_cubic(t)
        rope_img,rope_rect = rope_for_factor(rope_raw, earth_rect, f)
        surf.blit(rope_img, rope_rect)
    export_sequence("rope_grow", f4, draw_grow)

    pygame.quit(); sys.exit()

if __name__=="__main__":
    main()
