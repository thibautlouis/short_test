import manim as mn
import numpy as np
import manim_helper as mh
from drake_lang import t, LANG
from drake_title_card import show_title_card
import os

# --- Couleurs / tailles ---
GOLD = "#FFD700"
WHITE = "#FFFFFF"
ACCENT = "#50C878"
CAP_SCALE = 0.66  # taille fixe des légendes (aligne avec tes chapitres ~0.60–0.66)

# =========================
#  Helpers
# =========================


def _show_header_image(self, path: str, scale=1.15, buff=0.6, shift_down=0.5, rt=0.8):
    """Affiche une image au-dessus (fade-in). Stockée dans self._header_img."""
    img = mn.ImageMobject(path).scale(scale)
    img.to_edge(mn.UP, buff=buff).shift(mn.DOWN * shift_down)
    img.set_z_index(0)
    self.play(mn.FadeIn(img, shift=mn.DOWN*0.12), run_time=rt)
    # remplace l’ancienne si présente
    if getattr(self, "_header_img", None) is not None:
        self.remove(self._header_img)
    self._header_img = img

def _swap_header_image(self, path: str, scale=1.15, buff=0.6, shift_down=0.5, rt=0.8):
    """Remplace l’image d’en-tête actuelle par une autre (FadeOut/FadeIn)."""
    new_img = mn.ImageMobject(path).scale(scale)
    new_img.to_edge(mn.UP, buff=buff).shift(mn.DOWN * shift_down)
    new_img.set_z_index(0)
    cur = getattr(self, "_header_img", None)
    if cur is None:
        self.play(mn.FadeIn(new_img, shift=mn.DOWN*0.12), run_time=rt)
    else:
        self.play(mn.FadeOut(cur), mn.FadeIn(new_img, shift=mn.DOWN*0.12), run_time=rt)
        self.remove(cur)
    self._header_img = new_img

    try:
        self.add_to_center(new_img, bring_to_front=True)
    except Exception:
        if getattr(self, "_center_group", None) is None:
            self._center_group = mn.Group()
            self.add(self._center_group)
        if new_img not in self._center_group.submobjects:
            self._center_group.add(new_img)


def _make_term(tex, color=GOLD, scale=1.2, opacity=0.0):
    m = mn.MathTex(tex).set_color(color).scale(scale)
    m.set_opacity(opacity)
    return m

def _make_times(scale=1.1, opacity=0.0):
    m = mn.MathTex(r"\times").set_color(WHITE).scale(scale)
    m.set_opacity(opacity)
    return m

def _build_equation_row():
    """
    Construit l'équation entière dans UNE SEULE MathTex pour garantir
    une baseline commune, puis expose chaque morceau dans `parts`.
    Ordre : N, =, R_*, ×, f_p, ×, n_e, ×, f_l, ×, f_i, ×, f_c, ×, L
    """
    math = mn.MathTex(
        "N", "=", "R_\\ast", "\\times", "f_p", "\\times", "n_e",
        "\\times", "f_l", "\\times", "f_i", "\\times", "f_c", "\\times", "L"
    ).scale(1.2)

    # Couleurs & opacité initiale (0) pour animer ensuite
    operator_idx = {1, 3, 5, 7, 9, 11, 13}  # = et ×
    for i, sub in enumerate(math):
        sub.set_color(WHITE if i in operator_idx else GOLD)
        sub.set_opacity(0.0)

    # `row` = l'objet MathTex global ; `parts` = accès direct aux sous-mobjets
    row = math
    parts = [math[i] for i in range(len(math))]

    return row, parts
    
    
def _place_equation(self, row: mn.Mobject):
    mh.fit_into(row, self.anim_zone, pad=0.82, max_scale=1.0)

    # --- attacher au center group ---
    cg = getattr(self, "_center_group", None)
    if cg is None:
        cg = mn.Group()          # IMPORTANT: Group (pas VGroup) pour accepter ImageMobject
        self._center_group = cg
        self.add(cg)

    if row not in cg.submobjects:
        cg.add(row)

    # garder une ref si tu en as besoin ailleurs
    self._drake_row = row

def _make_caption_fixed(text: str, max_width: float) -> mn.Tex:
    """
    Légende à TAILLE FIXE (CAP_SCALE). Si une ligne dépasse max_width,
    on force 2 lignes (insertion '\\\\') sans changer l'échelle.
    """
    def build(s: str) -> mn.Tex:
        return mn.Tex(s).scale(CAP_SCALE).set_color(WHITE)

    # Respecter un éventuel '\\\\' fourni dans le texte
    if "\\\\" in text:
        m = build(text)
        if m.width <= max_width:
            return m

    single = build(text)
    if single.width <= max_width:
        return single

    # Wrap en 2 lignes proche du milieu
    words = text.replace("\\\\", " ").split()
    n = len(words)
    order = [n // 2]
    for d in range(1, n // 2 + 1):
        if n // 2 - d > 0:
            order.append(n // 2 - d)
        if n // 2 + d < n:
            order.append(n // 2 + d)
    for k in order:
        if 0 < k < n:
            cand = " ".join(words[:k]) + r"\\ " + " ".join(words[k:])
            m = build(cand)
            if m.width <= max_width:
                return m

    # fallback : couper au milieu
    k = max(1, min(n - 1, n // 2))
    cand = " ".join(words[:k]) + r"\\ " + " ".join(words[k:])
    return build(cand)

# =========================
#  Intro équation progressive
# =========================
def _intro_equation_animation(self):
    # --- Réglages temps (modifie juste ces constantes) ---
    FACTOR_FADE = 1   # durée du fondu d'un facteur (symbole + légende)
    FACTOR_HOLD = 1   # pause après apparition d'un facteur
    TIMES_FADE  = 0.5   # durée du fondu d'un "×"
    TIMES_HOLD  = 0.5   # pause après apparition d'un "×"
    EQUAL_FADE  = 0.5   # durée du fondu du "="
    EQUAL_HOLD  = 0.5   # pause après "="
    
    
    # Construire et placer la rangée d'équation
    row, parts = _build_equation_row()
    _place_equation(self, row)

    if getattr(self, "_drake_intro_caption", None) is not None:
        self.play(mn.FadeOut(self._drake_intro_caption, shift=mn.UP*0.05), run_time=0.45)
        self.remove(self._drake_intro_caption)
        self._drake_intro_caption = None


    # Tout invisible au départ
    for p in parts:
        p.set_opacity(0.0)

    # Zone de légende (utilise _make_caption_fixed si dispo)
    cap_zone = mn.Rectangle(width=row.width * 1.02, height=1.6,
                            stroke_opacity=0.0, fill_opacity=0.0)
    cap_zone.next_to(row, mn.DOWN, buff=0.35)
    self.add(cap_zone)

    # État
    shown = set()
    cap_current = None
    last_factor_idx = None

    def make_caption_obj(txt: str):
        if "_make_caption_fixed" in globals():
            cap = _make_caption_fixed(txt, max_width=cap_zone.width * 0.96)
        else:
            cap = mn.Tex(txt).scale(0.66).set_color(mn.WHITE)
        cap.move_to(cap_zone.get_center()).set_z_index(20).set_opacity(0.0)
        return cap

    def dim_all_except(active_idx):
        for j in shown:
            parts[j].set_opacity(1.0 if j == active_idx else 1)

    def show_factor(idx, cap_key):
        """Symbole + légende : fondu simultané linéaire, puis pause de lecture."""
        nonlocal cap_current, last_factor_idx
        # Prépare la légende
        new_cap = make_caption_obj(t(cap_key))
        self.add(new_cap)
        # Animations en parallèle (symbole + caption cross-fade)
        symbol_anim = parts[idx].animate.set_opacity(1.0)
        if cap_current is None:
            caption_anim = new_cap.animate.set_opacity(1.0)
        else:
            caption_anim = mn.AnimationGroup(
                cap_current.animate.set_opacity(0.0),
                new_cap.animate.set_opacity(1.0),
                lag_ratio=0.0
            )
        self.play(
            mn.AnimationGroup(symbol_anim, caption_anim, lag_ratio=0.0),
            run_time=FACTOR_FADE,
            rate_func=mn.rate_functions.linear   # fondu vraiment constant
        )
        cap_current = new_cap
        shown.add(idx)
        last_factor_idx = idx
        dim_all_except(last_factor_idx)
        self.wait(FACTOR_HOLD)

    def show_times(x_idx):
        """× seul : fondu linéaire, puis pause (la légende ne change pas)."""
        if x_idx not in shown:
            self.play(
                parts[x_idx].animate.set_opacity(1.0),
                run_time=TIMES_FADE,
                rate_func=mn.rate_functions.linear
            )
            shown.add(x_idx)
        # garder l'accent sur le dernier facteur
        if last_factor_idx is not None:
            dim_all_except(last_factor_idx)
        self.wait(TIMES_HOLD)

    # "=" (égal) : fondu puis pause
    def show_equal():
        if 1 not in shown:
            self.play(
                parts[1].animate.set_opacity(1.0),
                run_time=EQUAL_FADE,
                rate_func=mn.rate_functions.linear
            )
            shown.add(1)
        if last_factor_idx is not None:
            dim_all_except(last_factor_idx)
        self.wait(EQUAL_HOLD)

    # -------- déroulé --------
    show_factor(0, "lab_N")     # N
    show_equal()                # =
    show_factor(2, "lab_Rs")    # R*
    show_times(3)               # ×
    show_factor(4, "lab_fp")    # f_p
    show_times(5)               # ×
    show_factor(6, "lab_ne")    # n_e
    show_times(7)               # ×
    show_factor(8, "lab_fl")    # f_l
    show_times(9)               # ×
    show_factor(10, "lab_fi")   # f_i
    show_times(11)              # ×
    show_factor(12, "lab_fc")   # f_c
    show_times(13)              # ×
    show_factor(14, "lab_L")    # L

    self._drake_intro_caption = cap_current


    # rendre l’équation accessible aux autres étapes
    self._drake_row = row           # MathTex unique (baseline commune)
    self._drake_parts = [row[i] for i in range(len(row))]

    self.wait(1.0)
    
    

# =============================
#  Scène principale (Shorts)
# =============================
class ShortsManual(mh.TextChaptersScene):
    def construct(self):
        self.camera.background_color = mn.BLACK
        self.setup_layout()
        lang = os.getenv("SHORT_LANG", "FR")
        
        
        show_title_card(
            self,
            title_text=t("short_title"),  # prendra t("title") depuis drake_lang.py si dispo
            formula_tex=("math", r""),
            kepler_path="galaxy.png",  # ajuste le chemin si nécessaire
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",      # idem pour ton logo
            hold=1.0)

        
        chap0 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[],
        )
        self.show_chapter(chap0)

        _show_header_image(self, "galaxy.png", scale=0.15, buff=0.5, shift_down=1.5, rt=0.8)


        # --- Intro graphique progressive ---
        _intro_equation_animation(self)
        if getattr(self, "_drake_intro_caption", None) is not None:
            self.play(mn.FadeOut(self._drake_intro_caption, shift=mn.UP*0.05), run_time=0.45)
            self.remove(self._drake_intro_caption)
            self._drake_intro_caption = None

        # --- Texte principal ---
        chap1 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence01"),
                t("sentence02"),
                t("sentence03"),
                t("sentence04"),
                t("sentence05"),
                t("sentence06"),
                t("sentence07"),
            ],
        )
        self.show_chapter(chap1)
        self.wait(1)
        self.clear_text(bottom_only=True)
        _swap_header_image(
            self,
            "kepler.png",
            scale=0.3,
            buff=0.5,
            shift_down=2.6,
            rt=1.8
        )

        chap2 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence11"),
                t("sentence12"),
                t("sentence13"),
                t("sentence14"),
                ("text", t("sentence15"), {"color": (0, 0, 0, 0)}),
                t("sentence16"),
                t("sentence17"),
                t("sentence18"),

            ],
        )
        
        self.show_chapter(chap2)
        self.wait(2)
        self.clear_text(bottom_only=True)

        _swap_header_image(
            self,
            "SETI.png",
            scale=0.24,
            buff=0.5,
            shift_down=2.5,
            rt=1.8
        )

        chap3 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence20"),
                t("sentence21"),
                t("sentence22"),
                t("sentence23"),
                ("text", t("sentence24"), {"color": (1, 1, 1, 0)}),
                t("sentence25"),
                t("sentence26"),
                t("sentence27")])
        
        self.show_chapter(chap3)

      #  self.show_chapter(chap2)  # 'until=5' pour arrêter après sentence15 (exemple)

        # CTA
        cta = mn.Text(t("cta_sub"), color=mn.RED).scale(0.5)
        cta.next_to(self._title_current, mn.DOWN, buff=0.6)
        title_group = mn.VGroup(self._title_current, cta)
        self._title_current = title_group


        self.wait(3)
        self.play(mn.FadeIn(cta, shift=mn.DOWN*0.2), run_time=1)
        self.wait(5)

      #  self._center_group = VGroup(ax, x_label, y_label, graph)
        self.clear_text(clear_figure=True)
