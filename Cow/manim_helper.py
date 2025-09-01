import manim as mn
import numpy as np

# =============================
#  Helper Shorts 9:16 — layout commun, chapitres texte, pagination
# =============================

# --- Config vidéo (9:16, 1080x1920) ---
mn.config.frame_width  = 9
mn.config.frame_height = 16
mn.config.pixel_width  = 1080
mn.config.pixel_height = 1920

# ==========
# Constantes partagées
# ==========
PADDING = 0.96
LINE_BUFF = 0.24
TITLE_SCALE = 0.90
BOTTOM_SCALE = 0.60
BOTTOM_PAD = 0.93

class ChapterText:
    def __init__(self, title, bottom_lines):
        self.title = title
        self.bottom_lines = bottom_lines

def fit_into(mobj: mn.Mobject, box: mn.Mobject, pad=PADDING, max_scale=1.0):
    if mobj.width > 1e-9 and mobj.height > 1e-9:
        s = min((box.width*pad)/mobj.width, (box.height*pad)/mobj.height, max_scale)
        mobj.scale(s)
    mobj.move_to(box.get_center())
    return mobj

def place_top_anchor(group: mn.Mobject, box: mn.Mobject, y_off=0.08):
    cx = box.get_center()[0]
    cy = box.get_top()[1] - y_off - group.height/2
    group.move_to([cx, cy, 0])
    return group

def make_line(spec, scale=BOTTOM_SCALE):
    opts = {}
    if isinstance(spec, dict):
        kind = spec.get("type", "text")
        content = spec.get("content", "")
        opts = {k: v for k, v in spec.items() if k not in ("type", "content")}
        if kind.lower() == "math":
            mobj = mn.MathTex(content).scale(scale)
        else:
            mobj = mn.Tex(str(content)).scale(scale)
    elif isinstance(spec, tuple):
        if len(spec) == 2:
            kind, content = spec
        elif len(spec) == 3 and isinstance(spec[2], dict):
            kind, content, opts = spec
        else:
            kind, content = spec[0], spec[1]
        if kind.lower() == "math":
            mobj = mn.MathTex(content).scale(scale)
        else:
            mobj = mn.Tex(str(content)).scale(scale)
    else:
        mobj = mn.Tex(str(spec)).scale(scale)

    color = opts.get("color", None)
    if color is not None:
        mobj.set_color(color)
    mobj._line_opts = opts
    return mobj

class TextChaptersScene(mn.Scene):
    T_FADE   = 0.45
    T_WRITE  = 2.2
    T_PAUSE  = 0.25
    DEV_DEBUG = False

    def setup_layout(self):
        TITLE_H, ANIM_H, BOT_H = 1.2, 5.4, 7.4
        total = TITLE_H + ANIM_H + BOT_H
        top_center_y = total/2

        fw = 6.6
        self.title_zone = mn.Rectangle(width=fw, height=TITLE_H, stroke_opacity=0.0)
        self.anim_zone  = mn.Rectangle(width=fw, height=ANIM_H, stroke_opacity=0.0)
        self.bottom_zone= mn.Rectangle(width=fw, height=BOT_H, stroke_opacity=0.0)

        self.title_zone.move_to([0,  top_center_y - TITLE_H/2, 0])
        self.anim_zone.move_to([0,   top_center_y - TITLE_H - ANIM_H/2, 0])
        self.bottom_zone.move_to([0, - total/2 + BOT_H/2, 0])

        top_y = mn.config.frame_height / 2
        title_bottom_y = self.title_zone.get_bottom()[1]
        mask_height = top_y - title_bottom_y
        mask_center_y = (top_y + title_bottom_y) / 2
        self._title_mask = mn.Rectangle(
            width=mn.config.frame_width,
            height=mask_height,
            stroke_opacity=0.0,
            fill_color=mn.BLACK,
            fill_opacity=1.0,
        ).move_to([0, mask_center_y, 0])
        self._title_mask.set_z_index(10)
        self.add(self._title_mask)

        mask_height = self.bottom_zone.height + 1.0
        self._bottom_mask = mn.Rectangle(
            width=mn.config.frame_width,
            height=mask_height,
            stroke_opacity=0.0,
            fill_color=mn.BLACK,
            fill_opacity=1.0)
        self._bottom_mask.move_to(self.bottom_zone.get_center() - mn.UP * (mask_height - self.bottom_zone.height) / 2)
        self._bottom_mask.set_z_index(10)
        self.add(self._bottom_mask)

        if self.DEV_DEBUG:
            for z, c in [(self.title_zone, mn.BLUE), (self.anim_zone, mn.GREEN), (self.bottom_zone, mn.RED)]:
                z.set_stroke(c, opacity=0.7).set_fill(c, opacity=0.05)
                self.add(z)

        self._title_current = None
        self._bottom_page_current = None
        self._center_group = None

    def show_chapter(self, chap: ChapterText):
        title = mn.Tex(chap.title).scale(TITLE_SCALE)
        fit_into(title, self.title_zone, pad=0.96, max_scale=1.0)
        title.set_z_index(30)

        if self._title_current is None:
            self.play(mn.FadeIn(title, shift=mn.UP*0.1), run_time=self.T_FADE)
        else:
            self.play(mn.ReplacementTransform(self._title_current, title), run_time=self.T_FADE)
        self._title_current = title

        self._render_bottom_with_pagination(chap.bottom_lines)

    def clear_text(self, clear_figure: bool = False, bottom_only: bool = False, bottom_and_figure: bool = False):
        """
        Efface les éléments de texte.

        - Par défaut : efface le titre + le bas, et la figure si `clear_figure=True`.
        - Si `bottom_only=True` : n'efface QUE le texte du bas (ignore le titre).
        - Si `bottom_and_figure=True` : n'efface QUE le texte du bas ET la figure (ignore le titre).
        (Nouveau ; rétrocompatible. Si `bottom_only` et `bottom_and_figure` sont tous deux True,
        `bottom_and_figure` prévaut.)
        """
        # 1) Quoi effacer ?
        if bottom_and_figure:
            # Nouveau mode : ne touche pas au titre, mais efface le bas + la figure
            names = ["_bottom_page_current", "_chap_bottom_page_current", "_center_group"]
        elif bottom_only:
            # Mode historique : ne touche pas au titre ni à la figure
            names = ["_bottom_page_current", "_chap_bottom_page_current"]
        else:
            # Mode par défaut : efface titre + bas, et la figure si demandé
            names = ["_title_current", "_bottom_page_current", "_chap_bottom_page_current"]
            if clear_figure:
                names.append("_center_group")

        # 2) Collecter les mobjects présents
        items = [(name, getattr(self, name, None)) for name in names]
        items = [(name, mob) for name, mob in items if mob is not None]
        if not items:
            return

        # 3) Animer la disparition
        anims = [mn.FadeOut(mob, shift=mn.UP*0.05) for _, mob in items]
        self.play(*anims, run_time=self.T_FADE)

        # 4) Nettoyage (retirer de la scène + remettre les refs à None)
        self.remove(*[mob for _, mob in items])
        for name, _ in items:
            setattr(self, name, None)


    def _render_bottom_with_pagination(self, lines):
        max_h = self.bottom_zone.height * BOTTOM_PAD
        PAD_X = 0.96
        Y_OFF = 0.4

        def place_top_left(group: mn.Mobject):
            left_x = self.bottom_zone.get_left()[0] + (1 - PAD_X) * self.bottom_zone.width / 2
            top_y  = self.bottom_zone.get_top()[1] - Y_OFF
            dx = left_x - group.get_left()[0]
            dy = top_y  - group.get_top()[1]
            group.shift(mn.RIGHT * dx + mn.UP * dy)
            return group

        if self._bottom_page_current is not None:
            self.play(mn.FadeOut(self._bottom_page_current, shift=mn.UP*0.05), run_time=self.T_FADE)
            self._bottom_page_current = None

        page_items = []
        page_group = None

        for spec in lines:
            m = make_line(spec, scale=BOTTOM_SCALE)
            m.set_max_width(self.bottom_zone.width * PAD_X)

            test_items = page_items + [m]
            test_group = mn.VGroup(*test_items).arrange(mn.DOWN, aligned_edge=mn.LEFT, buff=LINE_BUFF)

            new_page_needed = not (test_group.height <= max_h or len(page_items) == 0)

            if new_page_needed:
                if page_group is not None:
                    self.play(mn.FadeOut(page_group, shift=mn.UP*0.06), run_time=self.T_FADE)
                    self.wait(0.10)
                page_items = [m]
                page_group = mn.VGroup(*page_items).arrange(mn.DOWN, aligned_edge=mn.LEFT, buff=LINE_BUFF)
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

            write_rt = getattr(m, "_line_opts", {}).get("write_rt", self.T_WRITE)
            self.play(mn.Write(m), run_time=write_rt)
            
            # --- New: fine-grained pause control ---
            _opts = getattr(m, "_line_opts", {})
            pause_before = _opts.get("pause_before", None)
            pause_after  = _opts.get("pause_after", None)
            pause_legacy = _opts.get("pause", None)  # kept for backward-compatibility
            
            # Optional pause BEFORE any animation
            if pause_before is not None:
                self.wait(pause_before)
            
            anim_fn = getattr(m, "_line_opts", {}).get("anim", None)
            if callable(anim_fn):
                anim_fn(self, m)
            
            # Default behavior:
            # - If an animation exists, apply 'pause' AFTER the animation.
            # - If no animation, 'pause' behaves as before (after the write).
            if pause_after is not None:
                self.wait(pause_after)
            elif pause_legacy is not None:
                self.wait(pause_legacy)
            else:
                self.wait(self.T_PAUSE)

        self._bottom_page_current = page_group
