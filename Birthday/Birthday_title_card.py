
import manim as mn
from typing import Optional, Union
import os
from birthday_lang import t


# --- Config vidéo (9:16, 1080x1920) ---
mn.config.frame_width  = 9
mn.config.frame_height = 16
mn.config.pixel_width  = 1080
mn.config.pixel_height = 1920

# --- Palette ---
BG    = mn.BLACK
WHITE = "#FFFFFF"
GOLD  = "#FFD700"

def _raise_z(m: mn.Mobject, z: int = 50):
    m.set_z_index(z)
    for sm in m.submobjects:
        _raise_z(sm, z)

def _make_rich_mobject(
    spec: Union[str, tuple, dict, mn.Mobject],
    *, default_color: str = GOLD, default_scale: float = 1.0
) -> mn.Mobject:
    """
    Construit un Mobject à partir de:
      - ("math", r"...") | ("text", "...")
      - {"type":"math"|"text", "content":"...", "scale": float?, "color": str?}
      - str simple => Tex
      - Mobject déjà construit => retourne tel quel
    """
    if isinstance(spec, mn.Mobject):
        return spec
    if isinstance(spec, tuple) and len(spec) >= 2:
        kind = str(spec[0]).lower()
        content = spec[1]
        m = mn.MathTex(content) if kind == "math" else mn.Tex(str(content))
        m.scale(default_scale).set_color(default_color)
        return m
    if isinstance(spec, dict):
        kind = str(spec.get("type", "text")).lower()
        content = spec.get("content", "")
        scale = float(spec.get("scale", default_scale))
        color = spec.get("color", default_color)
        m = mn.MathTex(content) if kind == "math" else mn.Tex(str(content))
        m.scale(scale).set_color(color)
        return m
    # str simple
    m = mn.Tex(str(spec))
    m.scale(default_scale).set_color(default_color)
    return m

# ---------- Builder ----------
def build_title_card_group(
    title_text: Optional[str] = None,
    formula_tex: Union[str, tuple, dict, mn.Mobject] = ("math", r"N = R_\star \, f_p \, n_e \, f_l \, f_i \, f_c \, L"),
    kepler_path: Optional[str] = "kepler.png",
    logo_path: Optional[str] = None,
) -> mn.Group:
    """
    Construit la title card (format SHORT 9:16) : grand titre, équation, png Kepler, puis logo.
    Positions fixes pour lisibilité et cohérence avec un layout Shorts.
    """
    items = []

    # --- Titre (grand, en haut)
    title_text = title_text or t("short_title")
    title = mn.Tex(title_text).set_color(WHITE).scale(1.3)
    title.move_to(mn.UP * 4.4)
    items.append(title)

    # --- Équation (juste sous le titre, bien lisible)
    formula = _make_rich_mobject(formula_tex, default_color=GOLD, default_scale=1)
    formula.move_to(mn.UP * 2.5)
    items.append(formula)

    # --- PNG Kepler (au centre)
    if kepler_path:
        try:
            kepler_img = mn.ImageMobject(kepler_path).scale(0.3)
            kepler_img.move_to(mn.UP * 0.2)
            items.append(kepler_img)
        except Exception as e:
            warn = mn.Tex("[kepler.png introuvable]").set_color("#FF6B6B").scale(0.6)
            warn.move_to(mn.UP * 0.2)
            items.append(warn)

    # --- Logo (en bas)
    if logo_path:
        try:
            logo = mn.ImageMobject(logo_path).scale(0.22)
            logo.move_to(mn.DOWN * 4.6)
            items.append(logo)
        except Exception as e:
            warn2 = mn.Tex("[logo introuvable]").set_color("#FF6B6B").scale(0.6)
            warn2.move_to(mn.DOWN * 4.6)
            items.append(warn2)

    group = mn.Group(*items)
    return group

def show_title_card(
    scene: mn.Scene,
    title_text: Optional[str] = None,
    formula_tex: Union[str, tuple, dict, mn.Mobject] = ("math", r"N = R_\star \, f_p \, n_e \, f_l \, f_i \, f_c \, L"),
    kepler_path: Optional[str] = "kepler.png",
    logo_path: Optional[str] = None,
    hold: float = 0.9,
) -> None:
    """
    Affiche la title card dans la scène, attend `hold`, puis fade out.
    """
    scene.camera.background_color = BG
    group = build_title_card_group(title_text, formula_tex, kepler_path, logo_path)
    _raise_z(group, 50)
    scene.add(group)
    scene.wait(hold)
    scene.play(mn.FadeOut(group), run_time=1.0)

# ---------- Test ----------
class BirthdayTitleCard(mn.Scene):
    def construct(self):
        self.camera.background_color = BG
        lang = os.getenv("SHORT_LANG", "FR")
        
        g = build_title_card_group(title_text=t("title"),
                                  formula_tex=("math", r""),
                                  kepler_path="birthday_cake.png",
                                  logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png")

        
        
        self.add(g)

