from manim import *
import manim_helper as mh
from time_dilatation_title_card import show_title_card
from frame_sequence_fit import FrameSequencePlayer
from time_dilatation_lang import t
import os




class ShortsTimeDilation(mh.TextChaptersScene):



    def play_triangle(self, L, v, c, dt):
        dx   = v * (dt/2.0)
        A    = np.array([0.0,   0.0, 0.0])      # départ bas
        B    = np.array([dx,    L,   0.0])      # haut
        C    = np.array([v*dt,  0.0, 0.0])      # retour bas
        foot = np.array([dx,    0.0, 0.0])      # pied de la verticale

        base   = Line(A, foot, color=WHITE,  stroke_width=2)
        vert   = Line(foot, B, color=WHITE,  stroke_width=2)

        # Lignes pointillées (compatibles 0.19.0)
        hyp_up = DashedLine(A, B, color=YELLOW, stroke_width=2, dash_length=0.2)  # AB
        hyp_dn = DashedLine(B, C, color=YELLOW, stroke_width=2, dash_length=0.2)  # BC

        right_angle = VGroup(
            Line(foot+0.3*LEFT, foot+0.3*LEFT+0.3*UP),
            Line(foot+0.3*UP,   foot+0.3*LEFT+0.3*UP)
        ).set_stroke(WHITE, 3)

        labA = MathTex("A").scale(0.3)
        labB = MathTex("B").scale(0.3)
        labC = MathTex("C").scale(0.3)
        
        var_name = {}
        var_name["FR"] = r"\Delta t_{\rm quai}"
        var_name["EN"] = r"\Delta t_{\rm platform}"
        var_name["ES"] = r"\Delta t_{\rm anden}"
        var_name["PT"] = r"\Delta t_{\rm plataforma}"
        
        
        LANG = os.getenv("SHORT_LANG", "FR")  # FR par défaut


        lab_base = MathTex(r"\tfrac{v\,%s}{2}" % var_name[LANG]).scale(0.35)
        lab_vert = MathTex(r"L").scale(0.35)
        lab_hyp  = MathTex(r"\tfrac{c\,%s}{2}" % var_name[LANG]).scale(0.35)

        # Grouper pour scale & centrage
        g = VGroup(base, vert, hyp_up, hyp_dn, right_angle,
                labA, labB, labC, lab_base, lab_vert, lab_hyp)
        target_h = self.anim_zone.height * 0.8
        if g.height > 1e-6:
            g.scale(target_h / g.height)
        g.move_to(self.anim_zone.get_center())

        # Repositionner labels après scale
        labA.next_to(base.get_start(), DOWN+LEFT, buff=0.2)
        labB.next_to(vert.get_end(),   UP+RIGHT,  buff=0.2)

        mid_AB = 0.5 * (A + B)
        lab_hyp.move_to(mid_AB + 3*UP + 3*LEFT)

        # get_end() marche souvent sur DashedLine, mais au pire remplacer par coord C
        labC.next_to(base.get_start(), DOWN + 38*RIGHT, buff=0.2)

        lab_base.next_to(base, DOWN, buff=0.25)
        lab_vert.next_to(vert, RIGHT, buff=0.25)

        # --- Ordre d’animation ---
        self.play(Create(hyp_up), run_time=0.9)                 # 1) AB (dash)
        self.play(Create(hyp_dn), run_time=0.9)                 # 2) BC (dash)
        self.play(Write(labA), Write(labB), Write(labC), run_time=0.7)  # 3) sommets
        self.play(Create(base), Create(vert), FadeIn(right_angle), run_time=0.8)  # 4) côtés pleins
        self.play(Write(lab_base), Write(lab_vert), Write(lab_hyp), run_time=0.8) # 5) labels
        self.wait(0.8)
        # NEW: regrouper pour pouvoir le supprimer d’un coup
        triangle = VGroup(
            base, vert, hyp_up, hyp_dn, right_angle,
            labA, labB, labC, lab_base, lab_vert, lab_hyp
        )
        triangle.set_z_index(5)

        # Option A: faire gérer par clear_text(...)
        self._center_group = triangle

        return triangle




    def construct(self):
        self.setup_layout()

        # Title card (même API que chez toi)
        show_title_card(
            self,
            title_text=t("title"),
            formula_tex=("math", r""),
            kepler_path="einstein.png",
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
            hold=1)

        pad = 0.98
        
        chap0 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[],
        )
        self.show_chapter(chap0)



        # --- Vidéo 1 : photon simple (miroirs fixes) ---
        video1 = FrameSequencePlayer(
            pattern="exports/clock_simple_td/frame_*.png",
            fps=60,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width*pad,
            max_h=self.anim_zone.height*pad,
            loop=False,
            autoplay=True,
            z=5,
        )
        self.add(video1)
        self.wait(len(video1.files) / video1.fps + 0.2)
        
        chap1 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence01"),
                t("sentence02"),
                t("sentence03"),
                t("sentence04"),
                t("sentence05"),
            ],
        )
        self.show_chapter(chap1)
        self.wait(3)
        
        self._center_group = video1

        self.clear_text(bottom_and_figure=True)

        # --- Vidéo 2 : miroirs dans le train ---
        video2 = FrameSequencePlayer(
            pattern="exports/train_lightclock/frame_*.png",
            fps=60,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width*2,
            max_h=self.anim_zone.height*2,
            loop=False,
            autoplay=False,
            z=5,
        )
        self.add(video2)

        chap2 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence11"),
                t("sentence12"),
                t("sentence13"),
                t("sentence14"),
                t("sentence15"),
            ],
        )
        self.show_chapter(chap2)

        # --- Vidéo 2 : miroirs dans le train ---
        video3 = FrameSequencePlayer(
            pattern="exports/train_lightclock/frame_*.png",
            fps=60,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width*2,
            max_h=self.anim_zone.height*2,
            loop=False,
            autoplay=True,
            z=5,
        )
        self.add(video3)
        self.wait(len(video3.files) / video2.fps + 0.2)

        self.remove(video2)
        self._center_group = video3

        self.clear_text(bottom_and_figure=True)

        # Appel de la fonction utilitaire
        tri = self.play_triangle(L=1.7, v=0.8, c=1.0, dt=4.0)


        chap3 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence21"),
                t("sentence22"),
                t("sentence23"),
                {"type": "text", "content":  t("sentence24"), "pause": 3},
                {"type": "text", "content":  t("sentence25"), "pause": 0.1},
                {"type": "text", "content":  t("sentence26"), "pause": 3},
                {"type": "text", "content":  t("sentence27"), "pause": 0.1},
            ],
        )
        self.show_chapter(chap3)
        self.wait(3)
        self.clear_text(bottom_and_figure=True)


        chap4 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence31"),
                t("sentence32"),
                t("sentence33"),
                {"type": "text", "content":  t("sentence34"), "pause": 2},
                t("sentence35"),
            ],
        )
        
        
        img = ImageMobject("einstein.png").scale(0.25)  # ton image
        img.set_z_index(5)
        img.scale_to_fit_height(self.anim_zone.height * 0.9)
        img.move_to(self.anim_zone.get_center())
        self.play(FadeIn(img, run_time=1.0))
        self._center_group = img  # pour que clear_text puisse la gérer



        self.show_chapter(chap4)
        
        cta = Text(t("cta_sub"), color=RED).scale(0.5)
        cta.next_to(self._title_current, 0.5*DOWN, buff=0.6)
        cta.set_z_index(10)

        title_group = VGroup(self._title_current, cta)
        self._title_current = title_group


        self.wait(3)
        self.play(FadeIn(cta, shift=DOWN*0.2), run_time=1)
        self.wait(5)

      #  self._center_group = VGroup(ax, x_label, y_label, graph)
        self.clear_text(clear_figure=True)
