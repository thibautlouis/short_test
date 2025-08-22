# pygame_quatuor_gameover_with_bag_and_numbers_fix.py
import os, glob, math, random
from pathlib import Path
import subprocess
import pygame as pg

# ----------------- CONFIG -----------------
RENDER_W, RENDER_H = 1080, 640
OUT_W, OUT_H = 720,  426   # taille cible pour l’animation dans Manim

PREVIEW_SCALE = 0.9
WIN_W, WIN_H = int(RENDER_W*PREVIEW_SCALE), int(RENDER_H*PREVIEW_SCALE)
FPS = 30
EXPORT_FRAMES = True
EXPORT_DIR = "exports/seq_quatuor_numbers"
BG_COLOR = (0, 0, 0)
# --- Export video settings ---
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = str((BASE_DIR / EXPORT_DIR).as_posix())  # make absolute
AUTO_MAKE_MP4 = True
MP4_PATH = str((BASE_DIR / "exports" / "seq_quatuor_numbers.mp4").as_posix())
FFMPEG_BIN = "ffmpeg"  # change if needed

# === Game Over (typewriter) config ===
GO_TEXT = "GAME OVER"
GO_LETTER_RATE = 14.0  # letters per second
GO_HOLD_TIME = 1.2     # seconds to hold after full text

CHAR_WALK_GLOB   = "assets/assets_prepped/assets_knight_simplewalk/walk_*.png"
CHEST_CLOSED     = "assets/assets_prepped/chest/closed.png"
CHEST_GOLD_GLOB  = "assets/assets_prepped/chest/full_open_*.png"
CHEST_EMPTY_GLOB = "assets/assets_prepped/chest/empty_open_*.png"
LOOT_BAG_PATH    = "assets/assets_prepped/loot_bag.png"

GRID_TOP, GRID_BOTTOM = 70, 570
COL_GAP = 320

STEP_FPS   = 6
CHEST_FPS  = 8
CHAR_SPEED = 400
PAUSE_FRAMES = 12

COIN_BURST = False  # garde simple

TAKE_GOLD = True
CLOSE_CHEST_AFTER = True
LOOT_DELAY_FRAMES = 10
CHEST_CLOSE_FPS = 10

EMPTY_ANIM_FPS  = 6
EMPTY_ANIM_TIME = 0.6

# Pixel number config
NUMBER_OFFSET = (30, 0)
NUMBER_PIXEL  = 3
NUMBER_COLOR  = (255, 0, 0)

# ----------------- HELPERS -----------------
def nn_scale(surf, scale):
    w, h = int(surf.get_width()*scale), int(surf.get_height()*scale)
    return pg.transform.scale(surf, (w,h))

def load_strip(pattern):
    files = sorted(glob.glob(pattern))
    return [pg.image.load(f).convert_alpha() for f in files] if files else []

def load_single(path):
    return pg.image.load(path).convert_alpha()

def blit_center(surface, sprite, center):
    rect = sprite.get_rect(center=center)
    surface.blit(sprite, rect)

def move_towards(pos, target, speed, dt):
    x, y = pos; tx, ty = target
    dx, dy = tx-x, ty-y
    dist = math.hypot(dx, dy)
    if dist < 1e-3: return (tx,ty), True
    step = speed*dt
    if step >= dist: return (tx,ty), True
    return (x+dx/dist*step, y+dy/dist*step), False


class SpriteAnim:
    def __init__(self, frames, fps=8, loop=True):
        self.frames = frames; self.fps = fps; self.loop = loop
        self.t = 0.0; self.index = 0
    def update(self, dt):
        self.t += dt*self.fps
        if self.loop:
            self.index = int(self.t) % len(self.frames)
        else:
            self.index = min(int(self.t), len(self.frames)-1)
    def current(self):
        return self.frames[self.index]

def layout_grid(chest_w, chest_h, gap_y, col_gap):
    cx = RENDER_W//2
    cy0 = GRID_TOP + chest_h//2
    centers = []
    for col in [-1,1]:
        x = cx + col*col_gap//2
        for row in range(3):
            y = cy0 + row*(chest_h+gap_y)
            centers.append((x,y))
    return centers

# --- Pixel-art digits (5x7) ---
DIGIT_5x7 = {
    "1": ["00100","01100","00100","00100","00100","00100","01110"],
    "2": ["01110","10001","00001","00010","00100","01000","11111"],
    "3": ["11110","00001","00001","01110","00001","00001","11110"],
    "4": ["00010","00110","01010","10010","11111","00010","00010"],
}
def draw_pixel_digit(surface, center_xy, digit, px=3, color=(255,255,255), outline=True):
    pat = DIGIT_5x7[str(digit)]
    w, h = 5, 7
    cx, cy = int(center_xy[0]), int(center_xy[1])
    x0 = cx - (w*px)//2
    y0 = cy - (h*px)//2
    if outline:
        shadow = (20,20,20)
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                for r,row in enumerate(pat):
                    for c,ch in enumerate(row):
                        if ch=="1":
                            rect = pg.Rect(x0+c*px+dx, y0+r*px+dy, px, px)
                            pg.draw.rect(surface, shadow, rect)
    for r,row in enumerate(pat):
        for c,ch in enumerate(row):
            if ch=="1":
                rect = pg.Rect(x0+c*px, y0+r*px, px, px)
                pg.draw.rect(surface, color, rect)

# ----------------- MP4 EXPORT -----------------
def _make_mp4_from_frames(export_dir, mp4_path, fps):
    # check if any frames exist
    frames = sorted(Path(export_dir).glob("frame_*.png"))
    if not frames:
        print(f"[export] No frames found in {export_dir} — skipping MP4.")
        return
    cmd = [
        FFMPEG_BIN, "-y",
        "-framerate", str(fps),
        "-i", str(Path(export_dir) / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        mp4_path
    ]
    print("[export] Running:", " ".join(str(c) for c in cmd))
    try:
        subprocess.run(cmd, check=True)
        print(f"[export] MP4 written to: {mp4_path}")
    except Exception as e:
        print("[export] ffmpeg failed:", e)

# ----------------- MAIN -----------------
def main():
    pg.init()
    screen = pg.display.set_mode((WIN_W, WIN_H))
    canvas = pg.Surface((RENDER_W, RENDER_H), pg.SRCALPHA)
    clock  = pg.time.Clock()
    Path(EXPORT_DIR).mkdir(parents=True, exist_ok=True)
    print(f"[export] Frames will be saved to: {EXPORT_DIR}")
    frame_id = 0

    # Assets
    walk_raw = load_strip(CHAR_WALK_GLOB); assert walk_raw
    chest_closed_raw = load_single(CHEST_CLOSED)
    gold_seq_raw  = load_strip(CHEST_GOLD_GLOB) or [chest_closed_raw]
    empty_seq_raw = load_strip(CHEST_EMPTY_GLOB) or [chest_closed_raw]

    loot_bag = None
    if LOOT_BAG_PATH and os.path.exists(LOOT_BAG_PATH):
        loot_bag = pg.image.load(LOOT_BAG_PATH).convert_alpha()

    # Scale
    h0 = chest_closed_raw.get_height()
    gap0 = int(h0 * 0.6)
    target_band = (GRID_BOTTOM - GRID_TOP)
    chest_scale = max(0.1, min(8.0, target_band / (3*h0 + 2*gap0)))

    chest_closed = nn_scale(chest_closed_raw, chest_scale)
    gold_seq  = [nn_scale(fr, chest_scale) for fr in gold_seq_raw]
    empty_seq = [nn_scale(fr, chest_scale) for fr in empty_seq_raw]

    # === Background sprite (user-provided) ===
    try:
        bg_raw = pg.image.load("assets/assets_prepped/background.png").convert()
        # Scale to cover screen while preserving aspect ratio; anchor bottom to keep flat ground
        scale = max(RENDER_W / bg_raw.get_width(), RENDER_H / bg_raw.get_height())
        bg = pg.transform.smoothscale(
            bg_raw,
            (int(bg_raw.get_width()*scale), int(bg_raw.get_height()*scale))
        )
        bg_rect = bg.get_rect()
        bg_rect.bottom = RENDER_H
        bg_rect.centerx = RENDER_W // 2
        print("[bg] Loaded background and scaled; bottom-aligned.")
    except Exception as e:
        bg = None
        print("[bg] Failed to load background:", e)

    chest_w, chest_h = chest_closed.get_width(), chest_closed.get_height()
    gap_y = int(chest_h * 0.40)

    char_scale = chest_scale * 1.15
    walk_frames = [nn_scale(fr, char_scale) for fr in walk_raw]
    anim_walk = SpriteAnim(walk_frames, fps=STEP_FPS, loop=True)

    if loot_bag is not None:
        char_h = walk_frames[0].get_height()
        scale = (char_h * 0.3) / loot_bag.get_height()
        loot_bag = nn_scale(loot_bag, scale)
    BAG_OFFSET = (0,30)

    centers = layout_grid(chest_w, chest_h, gap_y, COL_GAP)

    # Global chest state: "closed" or "empty" (empty = already looted)
    chest_global = ["closed"]*6

    # Targets: first 3 distinct, 4th repeats one (fails)
    distinct_idxs = [0,2,3]
    repeat_idx = distinct_idxs[1]
    targets = [distinct_idxs[0], distinct_idxs[1], distinct_idxs[2], repeat_idx]

    # Per-run vars
    current_person = 0
    target_idx = targets[current_person]
    spawn     = (RENDER_W//2, RENDER_H + 120)
    exit_top  = (RENDER_W//2, -120)
    char_pos = list(spawn)

    SIDE_CLEARANCE = 110
    def stop_point(idx):
        cx, cy = centers[idx]
        # idx 0,1,2 = colonne gauche ; 3,4,5 = colonne droite
        if idx >= 3:
            sx = cx - SIDE_CLEARANCE
        else:
            sx = cx
        sy = cy + chest_h // 2
        return (sx, sy)

    stop_open = stop_point(target_idx)

    # Local chest state per frame (visual FSM)
    # "opening_gold","gold","empty_anim","opening_empty","empty_open","empty","closed"
    chest_state_local = ["closed"]*6
    chest_t = [0]*6
    empty_anim_t = 0.0
    closing_t = 0.0
    gold_hold = 0
    has_loot = False
    pause = 0
    state = "approach"
    game_over = False
    game_over_timer = 45

    # --- Game Over typewriter state ---
    go_t = 0.0
    go_letters = 0
    go_done = False
    go_hold = 0.0

    # --- NEW: freeze visuel pendant le game over ---
    freeze_pos = None        # (x, y) figée du joueur
    freeze_frame = None      # frame sprite figée du joueur

    def reset_for_next():
        nonlocal chest_state_local, chest_t, empty_anim_t, closing_t, gold_hold, has_loot
        chest_state_local = ["closed"]*6
        chest_t = [0]*6
        empty_anim_t = 0.0
        closing_t = 0.0
        gold_hold = 0
        has_loot = False

    running = True
    while running:
        dt = clock.tick(FPS)/1000.0
        for e in pg.event.get():
            if e.type == pg.QUIT: running = False

        # ---------- FSM ----------
        if state == "approach":
            char_pos, arrived = move_towards(char_pos, stop_open, CHAR_SPEED, dt)
            anim_walk.update(dt)
            if arrived:
                state, pause = "pause_before", PAUSE_FRAMES

        elif state == "pause_before":
            pause -= 1
            if pause <= 0:
                # decide gold or empty based on global state
                if chest_global[target_idx] == "empty":
                    chest_state_local[target_idx] = "opening_empty"
                else:
                    chest_state_local[target_idx] = "opening_gold"
                chest_t[target_idx] = 0
                state = "open_chest"

        elif state == "open_chest":
            chest_t[target_idx] += 1
            if chest_state_local[target_idx] == "opening_gold":
                if chest_t[target_idx] >= len(gold_seq):
                    chest_state_local[target_idx] = "gold"
                    if TAKE_GOLD:
                        state = "hold_gold"; gold_hold = LOOT_DELAY_FRAMES
                    else:
                        state = "pause_after"; pause = PAUSE_FRAMES
            else:
                # opening empty for 4th knight → GAME OVER
                if chest_t[target_idx] >= len(empty_seq):
                    chest_state_local[target_idx] = "empty_open"
                    game_over = True
                    go_t = 0.0
                    go_letters = 0
                    go_done = False
                    go_hold = 0.0
                    # --- NEW: fige la position + frame du joueur
                    freeze_pos = (char_pos[0], char_pos[1])
                    try:
                        freeze_frame = anim_walk.current()
                    except Exception:
                        freeze_frame = None
                    state = "game_over"

        elif state == "hold_gold":
            gold_hold -= 1
            if gold_hold <= 0:
                has_loot = True
                chest_global[target_idx] = "empty"  # mark globally looted
                chest_state_local[target_idx] = "empty_anim"
                empty_anim_t = 0.0
                state = "empty_anim"

        elif state == "empty_anim":
            empty_anim_t += dt
            if empty_anim_t >= EMPTY_ANIM_TIME:
                if CLOSE_CHEST_AFTER and len(empty_seq) > 1:
                    state = "close_chest"; closing_t = len(empty_seq)-1
                else:
                    state = "pause_after"; pause = PAUSE_FRAMES

        elif state == "close_chest":
            closing_t -= CHEST_CLOSE_FPS * dt
            if closing_t <= 0:
                state = "pause_after"; pause = PAUSE_FRAMES

        elif state == "pause_after":
            pause -= 1
            if pause <= 0:
                state = "exit"

        elif state == "exit":
            char_pos, arrived = move_towards(char_pos, exit_top, CHAR_SPEED, dt)
            anim_walk.update(dt)
            if arrived:
                current_person += 1
                if current_person >= 4:
                    running = False
                else:
                    # next knight
                    reset_for_next()
                    target_idx = targets[current_person]
                    char_pos = list(spawn)
                    stop_open = stop_point(target_idx)
                    state = "approach"

        elif state == "game_over":
            # NEW: on NE recalcule PAS dt ici (garde le dt du clock.tick pour stabilité)
            if not go_done:
                go_t += dt
                go_letters = min(len(GO_TEXT), int(go_t * GO_LETTER_RATE))
                if go_letters >= len(GO_TEXT):
                    go_done = True
                    go_hold = GO_HOLD_TIME
            else:
                go_hold -= dt
                if go_hold <= 0:
                    running = False

        # ---------- Render ----------
        canvas.blit(bg, bg_rect) if bg is not None else canvas.fill(BG_COLOR)

        # Chests (draw empty as CLOSED visually, to avoid “disappear”)
        for i, c in enumerate(centers):
            st = chest_state_local[i]
            if st == "opening_gold":
                blit_center(canvas, gold_seq[min(chest_t[i], len(gold_seq)-1)], c)
            elif st == "gold":
                blit_center(canvas, gold_seq[-1], c)
            elif st == "empty_anim":
                if len(empty_seq) >= 3:
                    phase = int((EMPTY_ANIM_FPS * (empty_anim_t))) % 2
                    blit_center(canvas, empty_seq[1+phase], c)  # 1<->2 wiggle
                else:
                    blit_center(canvas, empty_seq[-1], c)
            elif st == "opening_empty":
                blit_center(canvas, empty_seq[min(chest_t[i], len(empty_seq)-1)], c)
            elif st == "empty_open":
                blit_center(canvas, empty_seq[-1], c)
            else:
                # show closed either for "closed" or global empty default look
                blit_center(canvas, chest_closed, c)

        # Closing overlay (play empty sequence backwards)
        if state == "close_chest":
            idx = max(0, int(round(closing_t)))
            blit_center(canvas, empty_seq[idx], centers[target_idx])

        # Knight + number + bag (stable en fin de partie)
        if game_over and freeze_pos is not None:
            kpos = freeze_pos
            kframe = freeze_frame if freeze_frame is not None else anim_walk.current()
        else:
            kpos = char_pos
            kframe = anim_walk.current()

        blit_center(canvas, kframe, kpos)
        digit = current_person + 1
        # arrondir pour éviter un snap subpixel
        num_pos = (int(round(kpos[0]+NUMBER_OFFSET[0])), int(round(kpos[1]+NUMBER_OFFSET[1])))
        draw_pixel_digit(canvas, num_pos, digit, px=NUMBER_PIXEL, color=NUMBER_COLOR, outline=True)
        if has_loot and loot_bag is not None:
            bag_rect = loot_bag.get_rect(center=(int(round(kpos[0]+BAG_OFFSET[0])),
                                                 int(round(kpos[1]+BAG_OFFSET[1]))))
            canvas.blit(loot_bag, bag_rect)

        # Game Over overlay (simple typewriter)
        if game_over:
            s = pg.Surface((RENDER_W, RENDER_H), pg.SRCALPHA)
            s.fill((0,0,0,110))
            canvas.blit(s, (0,0))
            font_big = pg.font.SysFont("arial", 100, bold=True)
            shown = GO_TEXT[:go_letters]
            txt = font_big.render(shown, True, (255, 80, 80))
            canvas.blit(txt, txt.get_rect(center=(RENDER_W//2, RENDER_H//2)))

        # ---------- Export / Preview ----------
        if EXPORT_FRAMES:
            frame_out = pg.transform.smoothscale(canvas, (OUT_W, OUT_H))
            pg.image.save(frame_out, os.path.join(EXPORT_DIR, f"frame_{frame_id:04d}.png"))
            if frame_id % 30 == 0:
                print(f"[export] saved frame_{frame_id:04d}.png")
            frame_id += 1

        preview = pg.transform.smoothscale(canvas, (WIN_W, WIN_H))
        screen.blit(preview,(0,0)); pg.display.flip()

    pg.quit()
    if AUTO_MAKE_MP4:
        _make_mp4_from_frames(EXPORT_DIR, MP4_PATH, FPS)

if __name__ == "__main__":
    main()
