from manim import *
import numpy as np
from manim_helper import *


class ShortsManual(TextChaptersScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.setup_layout()  # creates title_zone, anim_zone, bottom_zone
        self.add_sound("music.mp3")  # audio file must be in the same folder or full path

        chap0 = ChapterText(
            title="Euler: Infinite Product",
            bottom_lines=[],
        )
        self.show_chapter(chap0)

        ax = Axes(x_range=[-4*np.pi, 4*np.pi, np.pi], y_range=[-1, 1, 0.5], tips=False)
        x_label = Tex("$x$").scale(1.7).next_to(ax.x_axis.get_right(), UP, buff=0.2)
        y_label = Tex("$y$").scale(1.7).next_to(ax.y_axis.get_top(), RIGHT, buff=0.2)
        center_group = VGroup(ax, x_label, y_label)
        fit_into(center_group, self.anim_zone, pad=0.95)
        self.play(Create(ax), Write(VGroup(x_label, y_label)), run_time=1.0)

        # base functions
        f1 = lambda t: t**2 - 5*t + 6                    # blue
        f2 = lambda t: 0.05*(t**3 - 3*t)                  # coral
        f3 = lambda t: ((t-1)*(t+1)*(t-2)*(t+2))/4.0      # green quartic

        # horizontal offsets
        dx1, dx2, dx3 = -8.0, 0., 8

        g1 = ax.plot(lambda t: f1(t - dx1), color="#00BFFF", stroke_width=3)
        g2 = ax.plot(lambda t: f2(t - dx2), color="#FF7F50", stroke_width=3)
        g3 = ax.plot(lambda t: f3(t - dx3), color="#50C878", stroke_width=3)
        
        # animation
        self.play(Create(g1), Create(g2), Create(g3), run_time=3.0)

        graph = VGroup(g1, g2, g3)
        self.wait(0.3)
        
        chap1 = ChapterText(
            title="Euler: Infinite Product",
            bottom_lines=[
                r"When a polynomial $P(x)$ has roots $x_i \neq 0$:",
                {"type": "math",
                 "content":  r"P(x) = \mathrm{Cst} \times \prod_i\!\left(1-\frac{x}{x_i}\right)",
                 "pause": 4},
                r"For example: $P(x) = x^{2} - 5x + 6$",
                r"can be factored as $P(x) = 6(1 - x/2)(1 - x/3)$."
            ])
        self.show_chapter(chap1)
        self.wait(6)

        chap2 = ChapterText(
            title="Euler: Infinite Product",
            bottom_lines=[
                ("text", "Euler’s brilliant idea:", {"color": RED}),
                ("text",  "Treat $\\sin x$ just like a polynomial with known zeros.", {
                    "anim": lambda scene, line: scene.play(
                        Transform(
                            graph,
                            ax.plot(lambda x: np.sin(x), color=BLUE)
                        ), run_time=1.0)}),
                "The zeros of $\\sin x$ are $0,\\ \\pm\\pi,\\ \\pm 2\\pi,\\ \\pm 3\\pi,\\dots$",
                "So we can write it as:",
                {"type": "math",
                 "content":  r"\sin x = \mathrm{Cst} \times x\left(1-\frac{x}{\pi}\right)\left(1+\frac{x}{\pi}\right)\left(1-\frac{x}{2\pi}\right)\left(1+\frac{x}{2\pi}\right)\cdots"},
                {"type": "text",
                 "content":  "Each factor matches one zero of $\\sin x$.",
                 "pause": 4},
                "Pairing up the $\\pm n\\pi$ terms gives:",
                {
                    "type": "math",
                    "content":  r"\sin x = \mathrm{Cst} \times x\left(1-\frac{x^{2}}{\pi^{2}}\right)\left(1-\frac{x^{2}}{2^{2}\pi^{2}}\right)\left(1-\frac{x^{2}}{3^{2}\pi^{2}}\right)\cdots",
                    "pause": 4,
                },
                ("math", r"\lim_{x \to 0} \frac{\sin x}{x} = 1 \quad\Rightarrow\quad  \mathrm{Cst} = 1" ),
                ("math", r"\sin x = x\prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)"),
            ],
        )
        
        self.show_chapter(chap2)
        self.wait(10)
        self._center_group = VGroup(ax, x_label, y_label, graph)
        self.clear_text(clear_figure=True)
