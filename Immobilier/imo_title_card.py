import manim as mn
import os
from imo_lang import t, LANG

# --- Config vidéo (9:16, 1080x1920) ---
mn.config.frame_width  = 9
mn.config.frame_height = 16
mn.config.pixel_width  = 1080
mn.config.pixel_height = 1920

BG    = mn.BLACK
WHITE = "#FFFFFF"

def build_imo_title_card(
    title_text: str = t("title"),
    image_path: str = "money.png",
    logo_path: str = "/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
) -> mn.Group:
    items = []

    # --- Titre en haut ---
    title = mn.Tex(title_text).set_color(WHITE).scale(1.3)
    title.move_to(mn.UP * 4.4)
    items.append(title)

    # --- Image centrale (Deep Field) ---
    if image_path and os.path.exists(image_path):
        img = mn.ImageMobject(image_path).scale(0.7)
        img.move_to(mn.UP * 0.2)
        img.set_z_index(40)      # <-- z haut

        items.append(img)
    else:
        warn = mn.Tex("[image introuvable]").set_color("#FF6B6B").scale(0.4)
        warn.move_to(mn.UP * 0.2)
        items.append(warn)

    # --- Logo en bas ---
    if logo_path and os.path.exists(logo_path):
        logo = mn.ImageMobject(logo_path).scale(0.22)
        logo.move_to(mn.DOWN * 4.6)
        logo.set_z_index(40)      # <-- z haut

        items.append(logo)
    else:
        warn2 = mn.Tex("[logo introuvable]").set_color("#FF6B6B").scale(0.6)
        warn2.move_to(mn.DOWN * 4.6)
        items.append(warn2)

    return mn.Group(*items)

def show_imo_title_card(
    scene: mn.Scene,
    title_text: str = t("title"),
    image_path: str = "money.png",
    logo_path: str = "/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
    hold: float = 1.0,
):
    scene.camera.background_color = BG
    group = build_imo_title_card(title_text, image_path, logo_path)
    scene.add(group)
    scene.wait(hold)
    scene.play(mn.FadeOut(group), run_time=1.0)

# ---------- Exemple d’utilisation ----------
class TitleCard(mn.Scene):
    def construct(self):

        self.camera.background_color = mn.BLACK
        group = build_imo_title_card(title_text=t("title"),
                                           image_path="money.png",
                                           logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png")

        self.add(group)
