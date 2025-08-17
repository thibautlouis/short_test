# ./manim -pqh infinite_product.py ShortsManual
import manim as mn
import numpy as np
import manim_helper as mh
from infinite_product_lang import t
from infinite_product_lang import LANG
from infinite_product_title_card import show_title_card

class ShortsManual(mh.TextChaptersScene):

    def construct(self):
    
        show_title_card(
            self,
            title_text=t("title"),
            formula_tex=r"\sin x = x \prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)",
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
            hold=2,
        )

        self.camera.background_color = mn.BLACK
        self.setup_layout()  # crée title_zone, anim_zone, bottom_zone
        
      #  self.add_sound("/Users/louisthibaut/Desktop/projects/math_video/Music/blue_sea.mp3")

        chap0 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[],
        )
        self.show_chapter(chap0)

        ax = mn.Axes(x_range=[-4*np.pi, 4*np.pi, np.pi], y_range=[-1, 1, 0.5], tips=False)
        x_label = mn.Tex("$x$").scale(1.7).next_to(ax.x_axis.get_right(), mn.UP, buff=0.2)
        y_label = mn.Tex("$y$").scale(1.7).next_to(ax.y_axis.get_top(), mn.RIGHT, buff=0.2)
        center_group = mn.VGroup(ax, x_label, y_label)
        mh.fit_into(center_group, self.anim_zone, pad=0.95)
        self.play(mn.Create(ax), mn.Write(mn.VGroup(x_label, y_label)), run_time=1.0)

        # tes fonctions de base
        f1 = lambda t: t**2 - 5*t + 6                  # bleu
        f2 = lambda t: 0.05*(t**3 - 3*t)               # corail (quartique lisse)
        f3 = lambda t: ((t-1)*(t+1)*(t-2)*(t+2))/4.0   # vert (quartique factorisé)

        # offsets horizontaux (à ajuster)
        dx1, dx2, dx3 = -8.0, 0., 8

        g1 = ax.plot(lambda t: f1(t - dx1), color="#00BFFF", stroke_width=3)
        g2 = ax.plot(lambda t: f2(t - dx2), color="#FF7F50", stroke_width=3)
        g3 = ax.plot(lambda t: f3(t - dx3), color="#50C878", stroke_width=3)
        
        self.play(mn.Create(g1), mn.Create(g2), mn.Create(g3), run_time=3.0)

        graph = mn.VGroup(g1, g2, g3)
        self.wait(0.3)
        
        chap1 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[t("preamble"),
                         {"type": "math", "content":  t("poly_fact"), "pause": 2},
                         t("ex1"),
                         t("ex2")])
                         
        self.show_chapter(chap1)
        self.wait(6)

        chap2 = mh.ChapterText(
        title=t("title"),
        bottom_lines=[("text", t("euler_hook"), {"color": mn.BLUE}),
               ("text",   t("treat_poly"), {
                "anim": lambda scene, line: scene.play(
                    mn.Transform(
                        graph,
                        ax.plot(lambda x: np.sin(x), color=mn.BLUE)
                    ), run_time=1.0)}),
            t("sin_zeros"),
            t("so_write"),
            {"type": "math",
             "content":  t("sin_prod_1")},
            {"type": "text", "content":  t("each_factor"), "pause": 2},
            t("pairing"),
            {"type": "math", "content": t("sin_prod_2"), "pause": 2 },
            ("math", t("const_one")),
            ("math", t("final_prod"),  {"color": "#FFD700"}),
           ],
        )
        
        self.show_chapter(chap2)
        cta = mn.Text(t("cta_sub"), color=mn.RED).scale(0.5)
        cta.next_to(self._title_current, mn.DOWN, buff=0.6)

        title_group = mn.VGroup(self._title_current, cta)
        self._title_current = title_group

        self.wait(3)
        self.play(mn.FadeIn(cta, shift=mn.DOWN*0.2), run_time=1)
        self.wait(5)

        self._center_group = mn.VGroup(ax, x_label, y_label, graph)
        self.clear_text(clear_figure=True)
