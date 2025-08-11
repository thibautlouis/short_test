import manim as mn
import numpy as np
import math
import manim_helper as mh
from syracuse_lang import t, LANG
from syracuse_title_card import show_title_card  # optional


# --- helpers ---
def syracuse_sequence(u0, nmax=300, stop_at_cycle=True):
    u = int(u0)
    seq = [u]
    seen_1421 = 0
    for _ in range(nmax):
        u = (u // 2) if (u % 2 == 0) else (3*u + 1)
        seq.append(u)
        if stop_at_cycle:
            if u in (1, 2, 4):
                seen_1421 += 1
                if seen_1421 >= 3:
                    break
            else:
                seen_1421 = 0
    return seq


def _setup_syracuse_axes(self, u0_list):
    seqs = [syracuse_sequence(u0) for u0 in u0_list]
    max_len = max(len(s) for s in seqs) if seqs else 1
    max_val = max((max(s) for s in seqs if s), default=1)
    max_exp = max(0, math.ceil(math.log10(max_val if max_val > 0 else 1)))

    # Linear Y; we plot log10(u_n) to mimic log scale robustly
    ax = mn.Axes(
        x_range=[0, max_len - 1, max(1, (max_len - 1)//8 or 1)],
        y_range=[0, max_exp, 1],   # 0..max_exp (exp = log10)
        tips=False
    )
    xlab = mn.Tex("$n$").scale(1.4).next_to(ax.x_axis.get_right(), mn.RIGHT, buff=0.25)
    ylab = mn.Tex("$u_n$").scale(1.4).next_to(ax.y_axis.get_top(), mn.RIGHT+mn.UP, buff=0.25)
    grp = mn.VGroup(ax, xlab, ylab)
    mh.fit_into(grp, self.anim_zone, pad=0.95)

    # Pretty Y tick labels: 1, 10, 100, ...
    y_tick_labels = mn.VGroup(*[
        mn.MathTex(f"{10**e}").scale(0.6).next_to(ax.c2p(0, e), mn.LEFT, buff=0.08)
        for e in range(max_exp + 1)
    ])
    grp.add(y_tick_labels)
    x_step = max(1, (max_len - 1)//8 or 1)
    x_tick_labels = mn.VGroup(*[
        mn.MathTex(f"{int(x)}").scale(0.6).next_to(ax.c2p(x, 0), mn.DOWN, buff=0.08)
        for x in range(0, max_len, x_step)
    ])
    grp.add(x_tick_labels)

    # Curves (store color + data for real-time updates)
    colors = ["#00BFFF", "#FF7F50", "#50C878", "#FFD166", "#C084FC", "#FF6B6B"]
    plots = []
    for k, (u0, seq) in enumerate(zip(u0_list, seqs)):
        xs = list(range(len(seq)))
        ys_log = [math.log10(v if v > 0 else 1) for v in seq]  # plot log10
        col = colors[k % len(colors)]
        pl = ax.plot_line_graph(xs, ys_log, add_vertex_dots=False, line_color=col, stroke_width=3)
        pl._curve_color = col
        pl._u0_value = u0
        pl._xs = xs
        pl._ys_log = ys_log
        pl._seq_raw = seq
        plots.append(pl)

    self._syr_ax = ax
    self._syr_group = grp
    self._syr_plots = plots
    self._syr_drawn_axes = False

    # ---------- Compteur à largeur fixe (pas de rectangles visibles) ----------
    # Chiffre max de l'indice et de la valeur (toutes séquences confondues)
    self._idx_digits = max(1, len(str(max((len(s)-1) for s in seqs) if seqs else 0)))
    self._val_digits = max(1, len(str(max_val)))

    def _pad_left(num_str: str, total: int) -> str:
        pad = total - len(num_str)
        return (r"\phantom{" + "0"*pad + r"}" if pad > 0 else "") + num_str

    def _pad_right(num_str: str, total: int) -> str:
        pad = total - len(num_str)
        return num_str + (r"\phantom{" + "0"*pad + r"}" if pad > 0 else "")

    ur = ax.get_corner(mn.UR)
    self._u_anchor = mn.VectorizedPoint(ur + np.array([-0.25, -0.25, 0]))

    self._idx_digits = max(1, len(str(max((len(s)-1) for s in seqs) if seqs else 0)))
    self._val_digits = max(1, len(str(max_val)))

    idx0 = _pad_right("0", self._idx_digits)          # <-- padding à DROITE pour l’indice
    val0 = _pad_left("0", self._val_digits)           # <-- padding à GAUCHE pour la valeur
    self._u_counter = mn.MathTex(rf"u_{{{idx0}}} \;=\; {val0}").scale(0.9)

    self._u_counter.move_to(self._u_anchor, aligned_edge=mn.DR)
    self._u_counter.set_z_index(30)
    
    
    center_group = mn.VGroup()
    center_group.add(grp)
    for pl in plots:
        center_group.add(pl)
    center_group.add(self._u_counter)

    self._center_group = center_group


    return self._syr_group

def _syracuse_draw_seq(
    self,
    highlight_width=4,
    normal_width=3,
    dim_width=2,
    dim_opacity=0.35,
    hold_last=True,
    gap_between=0.35,
    step_slow=4.0,
):
    """Draw curves one-by-one; fixed counter shows u_n in real time (color = active curve)."""
    if not getattr(self, "_syr_drawn_axes", False):
        self.play(
            mn.Create(self._syr_ax),
            mn.Write(mn.VGroup(*[m for m in self._syr_group if m is not self._syr_ax])),
            run_time=0.6
        )
        self._syr_drawn_axes = True

    prev_pl = None
    for _, pl in enumerate(self._syr_plots):
        col = getattr(pl, "_curve_color", mn.WHITE)
        xs = pl._xs
        ys_log = pl._ys_log
        seq_raw = pl._seq_raw

        if self._u_counter not in self.mobjects:
            self.add(self._u_counter)

        if prev_pl is not None:
            self.play(prev_pl.animate.set_stroke(opacity=dim_opacity, width=dim_width), run_time=0.25)

        tracker = mn.ValueTracker(0)

        dot = mn.Dot(color=col, radius=0.055).set_z_index(25)
        def dot_updater(d):
            i = int(np.clip(round(tracker.get_value()), 0, len(xs)-1))
            d.move_to(self._syr_ax.c2p(xs[i], ys_log[i]))
        dot.add_updater(dot_updater)
        self.add(dot)
        
        if getattr(self, "_center_group", None) is not None:
            self._center_group.add(dot)

        
        def counter_updater(m):
            i = int(np.clip(round(tracker.get_value()), 0, len(xs)-1))

            # mêmes helpers que ci-dessus
            def _pad_left(num_str: str, total: int) -> str:
                pad = total - len(num_str)
                return (r"\phantom{" + "0"*pad + r"}" if pad > 0 else "") + num_str

            def _pad_right(num_str: str, total: int) -> str:
                pad = total - len(num_str)
                return num_str + (r"\phantom{" + "0"*pad + r"}" if pad > 0 else "")

            idx_tex = _pad_right(str(i), getattr(self, "_idx_digits", 1))            # <-- droite
            val_tex = _pad_left(str(seq_raw[i]), getattr(self, "_val_digits", 1))    # <-- gauche

            new_tex = mn.MathTex(rf"u_{{{idx_tex}}} \;=\; {val_tex}").scale(0.9).set_color(col)
            new_tex.move_to(self._u_anchor, aligned_edge=mn.DR)
            m.become(new_tex)

        self._u_counter.add_updater(counter_updater)

        npts = len(xs)
        base_rt = max(0.8, min(2.2, 0.04*npts))
        rt = base_rt * float(step_slow)

        self.play(
            mn.Create(pl.set_stroke(width=highlight_width)),
            tracker.animate.set_value(len(xs)-1),
            run_time=rt
        )

        dot.remove_updater(dot_updater)
        self._u_counter.remove_updater(counter_updater)
        self.remove(dot)

        if hold_last is False or pl is not self._syr_plots[-1]:
            self.play(pl.animate.set_stroke(width=normal_width), run_time=0.15)

        if pl is not self._syr_plots[-1]:
            self.wait(gap_between)

        prev_pl = pl


# =============================
class ShortsManual(mh.TextChaptersScene):
    def construct(self):
        self.camera.background_color = mn.BLACK
        self.setup_layout()

        # (optional) show_title_card(self, title=t("title"))

        # --- Titre initial ---
        self.show_chapter(mh.ChapterText(title=t("title"), bottom_lines=[]))

        # --- Dessin des axes seuls ---
        u0_list = [5, 15, 23]  # on prépare tout pour que les dimensions soient correctes
        _setup_syracuse_axes(self, u0_list)

        # Animation axes + labels seulement
        self.play(
            mn.Create(self._syr_ax),
            mn.Write(mn.VGroup(*[m for m in self._syr_group if m is not self._syr_ax])),
            run_time=0.6
        )
        self._syr_drawn_axes = True  # pour que _syracuse_draw_seq ne les redessine pas

        # --- Narration principale ---
        from types import MethodType
        self._syracuse_draw_seq = MethodType(_syracuse_draw_seq, self)

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
