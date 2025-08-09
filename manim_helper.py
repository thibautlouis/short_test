# manim_helper.py
from manim import *
import numpy as np

# =============================
#  Helper Shorts 9:16 — layout commun, chapitres texte, pagination
# =============================

# --- Config vidéo (9:16, 1080x1920) ---
config.frame_width  = 9
config.frame_height = 16
config.pixel_width  = 1080
config.pixel_height = 1920

# ==========
# Constantes partagées
# ==========
PADDING = 0.96        # marge intérieure relative pour fit
LINE_BUFF = 0.24      # espacement entre lignes du bas
TITLE_SCALE = 0.90    # échelle de base du titre
BOTTOM_SCALE = 0.60   # échelle de base du bas
BOTTOM_PAD = 0.93     # part de la hauteur utilisable (pagination)

class ChapterText:
    """Un “chapitre” **texte uniquement** : titre (haut) + bloc bas (multi-lignes, paginé)."""
    def __init__(self, title, bottom_lines):
        self.title = title
        self.bottom_lines = bottom_lines  # list[str | ('math','...')[, opts] | ('text','...')[, opts]]


def fit_into(mobj: Mobject, box: Mobject, pad=PADDING, max_scale=1.0):
    if mobj.width > 1e-9 and mobj.height > 1e-9:
        s = min((box.width*pad)/mobj.width, (box.height*pad)/mobj.height, max_scale)
        mobj.scale(s)
    mobj.move_to(box.get_center())
    return mobj

def place_top_anchor(group: Mobject, box: Mobject, y_off=0.08):
    cx = box.get_center()[0]
    cy = box.get_top()[1] - y_off - group.height/2
    group.move_to([cx, cy, 0])
    return group

def make_line(spec, scale=BOTTOM_SCALE):
    """
    Formats acceptés (compatibles avec l'existant) :
      - str                                  -> Tex
      - ('math', r'...')                     -> MathTex
      - ('tex',  '...')                      -> Tex
      - ('math', r'...', {'color': ..., 'write_rt': ..., 'pause': ..., 'anim': callable})
      - ('text', '...',  {'color': ..., 'write_rt': ..., 'pause': ..., 'anim': callable})
      - dict: {
            "type": "math"|"text",           # défaut: "text"
            "content": r"...",               # obligatoire
            "color": ...,
            "write_rt": float,               # durée d'écriture de la ligne
            "pause": float,                  # pause après écriture
            "anim": callable(scene, line),   # animation à jouer juste après la ligne
        }
    """
    opts = {}

    # --- Nouveau: format dict ---
    if isinstance(spec, dict):
        kind = spec.get("type", "text")
        content = spec.get("content", "")
        # toutes les autres clés deviennent des options
        opts = {k: v for k, v in spec.items() if k not in ("type", "content")}
        if kind.lower() == "math":
            mobj = MathTex(content).scale(scale)
        else:
            mobj = Tex(str(content)).scale(scale)

    # --- Formats existants: tuple / str ---
    elif isinstance(spec, tuple):
        if len(spec) == 2:
            kind, content = spec
        elif len(spec) == 3 and isinstance(spec[2], dict):
            kind, content, opts = spec
        else:
            kind, content = spec[0], spec[1]
        if kind.lower() == "math":
            mobj = MathTex(content).scale(scale)
        else:
            mobj = Tex(str(content)).scale(scale)
    else:
        mobj = Tex(str(spec)).scale(scale)

    # Couleur optionnelle
    color = opts.get("color", None)
    if color is not None:
        mobj.set_color(color)

    # stocker les options pour la phase d'animation
    mobj._line_opts = opts
    return mobj

# ==========
# Scène de base (zones, chapitres, pagination, clear)
# ==========
class TextChaptersScene(Scene):
    # Durées (adapter si besoin)
    T_FADE   = 0.45
    T_WRITE  = 3
    T_PAUSE  = 0.25
    DEV_DEBUG = False  # True pour afficher les zones

    def setup_layout(self):
        """Crée les zones fixes (haut/centre/bas). Appeler une seule fois au début."""
        # Ratios “trois bandes” adaptés Shorts (à ajuster selon ta charte exacte)
        TITLE_H, ANIM_H, BOT_H = 1.2, 5.4, 7.4
        total = TITLE_H + ANIM_H + BOT_H
        top_center_y = total/2

        fw = 6.6  # largeur utile (safe area)
        self.title_zone = Rectangle(width=fw, height=TITLE_H, stroke_opacity=0.0)
        self.anim_zone  = Rectangle(width=fw, height=ANIM_H, stroke_opacity=0.0)
        self.bottom_zone= Rectangle(width=fw, height=BOT_H, stroke_opacity=0.0)

        self.title_zone.move_to([0,  top_center_y - TITLE_H/2, 0])
        self.anim_zone.move_to([0,   top_center_y - TITLE_H - ANIM_H/2, 0])
        self.bottom_zone.move_to([0, - total/2 + BOT_H/2, 0])

        # === Masque "haut de short" (entre bas du titre et bord haut) ===
        top_y = config.frame_height / 2
        title_bottom_y = self.title_zone.get_bottom()[1]
        mask_height = top_y - title_bottom_y
        mask_center_y = (top_y + title_bottom_y) / 2
        self._title_mask = Rectangle(
            width=config.frame_width,
            height=mask_height,
            stroke_opacity=0.0,
            fill_color=BLACK,
            fill_opacity=1.0,
        ).move_to([0, mask_center_y, 0])
        self._title_mask.set_z_index(10)
        self.add(self._title_mask)
        
                
        mask_height = self.bottom_zone.height + 1.0  # ajuste 1.0 selon besoin

        self._bottom_mask = Rectangle(
            width=config.frame_width,
            height=mask_height,
            stroke_opacity=0.0,
            fill_color=BLACK,
            fill_opacity=1.0)

        # Le positionner de façon à couvrir jusqu'en bas
        self._bottom_mask.move_to(self.bottom_zone.get_center() - UP * (mask_height - self.bottom_zone.height) / 2)

        self._bottom_mask.set_z_index(10)
        self.add(self._bottom_mask)


        if self.DEV_DEBUG:
            for z, c in [(self.title_zone, BLUE), (self.anim_zone, GREEN), (self.bottom_zone, RED)]:
                z.set_stroke(c, opacity=0.7).set_fill(c, opacity=0.05)
                self.add(z)

        # États actuels (références pour remplacement/clear)
        self._title_current = None
        self._bottom_page_current = None
        self._center_group = None   # à remplir dans tes scènes spécifiques si tu veux clear la figure

    # ========== API TEXTE SEULE ==========
    def show_chapter(self, chap: ChapterText):
        """
        Affiche/replace le **titre** et le **bloc bas** (avec pagination).
        Ne touche **pas** à la zone d'animation centrale : tu restes libre.
        """
        # ----- TITRE -----
        title = Tex(chap.title).scale(TITLE_SCALE)
        fit_into(title, self.title_zone, pad=0.96, max_scale=1.0)
        title.set_z_index(30)  # au-dessus du masque

        if self._title_current is None:
            self.play(FadeIn(title, shift=UP*0.1), run_time=self.T_FADE)
        else:
            self.play(ReplacementTransform(self._title_current, title), run_time=self.T_FADE)
        self._title_current = title

        # ----- BAS (pagination) -----
        self._render_bottom_with_pagination(chap.bottom_lines)

    def clear_text(self, clear_figure=False):
        """Efface le titre, le bloc bas et (optionnellement) la figure centrale en même temps."""
        anims = []

        # ----- Titre -----
        if getattr(self, "_title_current", None) is not None:
            anims.append(FadeOut(self._title_current, shift=UP*0.05))
            self.remove(self._title_current)
            self._title_current = None

        # ----- Bas (2 noms possibles, compat) -----
        if getattr(self, "_bottom_page_current", None) is not None:
            anims.append(FadeOut(self._bottom_page_current, shift=UP*0.05))
            self.remove(self._bottom_page_current)
            self._bottom_page_current = None

        if getattr(self, "_chap_bottom_page_current", None) is not None:
            anims.append(FadeOut(self._chap_bottom_page_current, shift=UP*0.05))
            self.remove(self._chap_bottom_page_current)
            self._chap_bottom_page_current = None

        # ----- Figure centrale -----
        if clear_figure and getattr(self, "_center_group", None) is not None:
            anims.append(FadeOut(self._center_group, shift=UP*0.05))
            self.remove(self._center_group)
            self._center_group = None

        # ----- Animation groupée -----
        if anims:
            self.play(*anims, run_time=self.T_FADE)

    # ========== Interne : rendu bas paginé (avec couleur + anim/ligne) ==========
    def _render_bottom_with_pagination(self, lines):
        max_h = self.bottom_zone.height * BOTTOM_PAD
        PAD_X = 0.96
        Y_OFF = 0.4

        def place_top_left(group: Mobject):
            left_x = self.bottom_zone.get_left()[0] + (1 - PAD_X) * self.bottom_zone.width / 2
            top_y  = self.bottom_zone.get_top()[1] - Y_OFF
            dx = left_x - group.get_left()[0]
            dy = top_y  - group.get_top()[1]
            group.shift(RIGHT * dx + UP * dy)
            return group

        # Efface la page précédente si présente
        if self._bottom_page_current is not None:
            self.play(FadeOut(self._bottom_page_current, shift=UP*0.05), run_time=self.T_FADE)
            self._bottom_page_current = None

        page_items = []
        page_group = None

        for spec in lines:
            m = make_line(spec, scale=BOTTOM_SCALE)
            m.set_max_width(self.bottom_zone.width * PAD_X)

            test_items = page_items + [m]
            test_group = VGroup(*test_items).arrange(DOWN, aligned_edge=LEFT, buff=LINE_BUFF)

            new_page_needed = not (test_group.height <= max_h or len(page_items) == 0)

            if new_page_needed:
                if page_group is not None:
                    self.play(FadeOut(page_group, shift=UP*0.06), run_time=self.T_FADE)
                    self.wait(0.10)
                page_items = [m]
                page_group = VGroup(*page_items).arrange(DOWN, aligned_edge=LEFT, buff=LINE_BUFF)
                place_top_left(page_group)
                self.add(page_group)
            else:
                page_items.append(m)
                page_group = test_group
                place_top_left(page_group)
                if len(page_items) == 1:
                    self.add(page_group)
                else:
                    self.add(m)
        
            page_group.set_z_index(20)

            # --- écriture de la ligne avec durée optionnelle ---
            write_rt = getattr(m, "_line_opts", {}).get("write_rt", self.T_WRITE)
            self.play(Write(m), run_time=write_rt)
            pause_time = getattr(m, "_line_opts", {}).get("pause", self.T_PAUSE)
            self.wait(pause_time)

            # --- animation optionnelle associée à cette ligne ---
            line_opts = getattr(m, "_line_opts", {})
            anim_fn = line_opts.get("anim", None)
            if callable(anim_fn):
                anim_fn(self, m)

        self._bottom_page_current = page_group
