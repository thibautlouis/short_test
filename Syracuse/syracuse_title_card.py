# syracuse_title_card.py
import manim as mn
from typing import Iterable, Optional, Union
from syracuse_lang import t
import os

# --- Config vidéo (9:16, 1080x1920) ---
mn.config.frame_width  = 9
mn.config.frame_height = 16
mn.config.pixel_width  = 1080
mn.config.pixel_height = 1920

BG = mn.BLACK
GOLD = "#FFD700"
WHITE = "#FFFFFF"
COLORS = ["#00BFFF", "#FF7F50", "#50C878", "#FFD166", "#C084FC", "#FF6B6B"]

# ---------- utils ----------
def _syracuse_sequence(u0: int, nmax: int = 25) -> list[int]:
    """Retourne la suite (u_n) en partant de u0, tronquée à nmax, arrêtée à 1 si atteint."""
    u = int(u0)
    seq = [u]
    for _ in range(nmax):
        if u == 1:
            break
        u = u // 2 if (u % 2 == 0) else (3 * u + 1)
        seq.append(u)
    return seq

def _make_rich_mobject(
    spec: Union[str, tuple, dict, mn.Mobject],
    *,
    default_color: str = GOLD,
    default_scale: float = 1.0,
) -> mn.Mobject:
    """
    Crée un Mobject à partir de:
      - ("math", r"...") | ("text", "...")
      - {"type":"math"|"text", "content":"...", "scale": float?, "color": str?}
      - string simple
      - Mobject déjà construit (Tex, MathTex, VGroup…)
    Applique color/scale si fourni; sinon valeurs par défaut.
    """
    # Si c'est déjà un Mobject → le retourner directement
    if isinstance(spec, mn.Mobject):
        return spec

    # tuple ("math", "...") / ("text", "...")
    if isinstance(spec, tuple) and len(spec) >= 2:
        kind = str(spec[0]).lower()
        content = spec[1]
        m = mn.MathTex(content) if kind == "math" else mn.Tex(str(content))
        m.scale(default_scale).set_color(default_color)
        return m

    # dict {"type":..., "content":..., "scale":..., "color":...}
    if isinstance(spec, dict):
        kind = str(spec.get("type", "text")).lower()
        content = spec.get("content", "")
        scale = float(spec.get("scale", default_scale))
        color = spec.get("color", default_color)
        m = mn.MathTex(content) if kind == "math" else mn.Tex(str(content))
        m.scale(scale).set_color(color)
        return m

    # string simple => Tex
    m = mn.Tex(str(spec))
    m.scale(default_scale).set_color(default_color)
    return m

def _raise_z(m: mn.Mobject, z: int = 50):
    m.set_z_index(z)
    for sm in m.submobjects:
        _raise_z(sm, z)

def make_quote(text: str, author: str, lang="FR", color="#3B82F6", scale=0.9) -> mn.VGroup:
    """Crée un bloc citation avec guillemets, texte sur 2 lignes et auteur."""
    # Guillemets selon la langue
    quotes = {
        "FR": ("« ", " »"),
        "EN": ("“", "”"),
        "ES": ("« ", " »"),
        "PT": ("« ", " »"),
    }
    lq, rq = quotes.get(lang, ("“", "”"))

    # Séparation en deux lignes automatiques
    words = text.split()
    mid = len(words) // 2
    line1 = " ".join(words[:mid])
    line2 = " ".join(words[mid:])
    latex_text = f"{lq}{line1}\\\\{line2}{rq}"

    quote_tex = mn.Tex(latex_text).scale(scale).set_color(color)
    author_tex = mn.Tex(f"— {author}").scale(scale * 0.7).set_color(color)

    group = mn.VGroup(quote_tex, author_tex).arrange(mn.DOWN, buff=0.3)
    return group

# ---------- builder ----------
def build_title_card_group(
    title_text: str,
    formula_tex,
    logo_path: Optional[str] = None,
    u0_list: Optional[Iterable[int]] = None,
) -> mn.Group:
    """Construit la title card avec titre, bloc central (math ou texte ou citation), graphe et logo."""
    items = []

    # --- Titre
    title = mn.Tex(title_text).set_color(WHITE).scale(1.05)
    title.move_to(mn.UP * 4.0)
    items.append(title)

    # --- Bloc central
    formula = _make_rich_mobject(formula_tex, default_color=GOLD, default_scale=1.0)
    formula.move_to(mn.UP * 2.0)
    items.append(formula)

    # --- Graphe optionnel
    if u0_list:
        seqs = [_syracuse_sequence(int(u0), nmax=25) for u0 in u0_list]
        max_len = max(len(s) for s in seqs) if seqs else 1
        max_val = max((max(s) for s in seqs if s), default=1)
        y_cap = min(max_val, 200)
        step_x = max(1, (max_len - 1) // 8 or 1)
        step_y = max(1, y_cap // 5 or 1)

        ax = mn.Axes(
            x_range=[0, max_len - 1, step_x],
            y_range=[0, y_cap, step_y],
            tips=False,
        ).scale(0.5)
        ax.move_to(mn.DOWN * 0.7)

        plots = []
        for k, (u0, seq) in enumerate(zip(u0_list, seqs)):
            xs = list(range(len(seq)))
            ys = seq
            col = COLORS[k % len(COLORS)]
            pl = ax.plot_line_graph(xs, ys, add_vertex_dots=False, line_color=col, stroke_width=3)
            plots.append(pl)
            if xs:
                lbl = mn.MathTex(rf"u_0={u0}").scale(0.5).set_color(col)
                lbl.next_to(ax.c2p(xs[0], ys[0]), mn.LEFT, buff=0.08)
                plots.append(lbl)

        xlab = mn.Tex("$n$").scale(0.9).next_to(ax.x_axis.get_right(), mn.UP, buff=0.15)
        ylab = mn.Tex("$u_n$").scale(0.9).next_to(ax.y_axis.get_top(), mn.RIGHT, buff=0.15)

        graph_group = mn.VGroup(ax, xlab, ylab, *plots)
        items.append(graph_group)

    # --- Logo optionnel
    if logo_path:
        logo = mn.ImageMobject(logo_path).scale(0.2)
        logo.move_to(mn.DOWN * 4.0)
        items.append(logo)

    return mn.Group(*items)

# ---------- API ----------
def show_title_card(
    scene: mn.Scene,
    title_text: str,
    formula_tex,
    logo_path: Optional[str] = None,
    u0_list: Optional[Iterable[int]] = None,
    hold: float = 0.7,
) -> None:
    """Affiche la title card dans la scène, attend `hold`, puis fade out."""
    scene.camera.background_color = BG
    group = build_title_card_group(title_text, formula_tex, logo_path, u0_list)
    _raise_z(group, 50)
    scene.add(group)
    scene.wait(hold)
    scene.play(mn.FadeOut(group), run_time=1.0)

# ---------- test ----------
class TitleCard(mn.Scene):
    def construct(self):
        self.camera.background_color = BG
        
        lang = os.getenv("SHORT_LANG", "FR")

        g = build_title_card_group(
            title_text=t("title"),
            formula_tex=make_quote(
                text=t("sentence13")["content"],
                author="Paul Erdős",
                lang=lang,
                color="#FFD166",
                scale=0.85,
            ),
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
            u0_list=[7, 11, 3],
        )
        self.add(g)
