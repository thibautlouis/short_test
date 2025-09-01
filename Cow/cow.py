from manim import *
import manim_helper as mh
from frame_sequence_fit import FrameSequencePlayer
from cow_lang import t
import os
from manim import Tex, MathTex, TexTemplate
from cow_title_card import show_title_card

tex = TexTemplate()
tex.add_to_preamble(r"\usepackage{amsmath}")  # utile si tu utilises aligned ailleurs
tex.add_to_preamble(r"\usepackage{xcolor}")   # nécessaire pour \textcolor / \color
Tex.set_default(tex_template=tex)
MathTex.set_default(tex_template=tex)

class Shortsvache(mh.TextChaptersScene):

    def construct(self):
        self.setup_layout()


        show_title_card(
            self,
            title_text=t("title"),
            formula_tex=("math", r""),
            kepler_path="cow_pic.png",
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
            hold=1)
            
        pad = 0.98
        
        chap0 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[],
        )
        self.show_chapter(chap0)
        
        

        
        

        img = ImageMobject("sortie_frames/frame_00000.png")
        img.set_z_index(5)
        img.scale_to_fit_height(self.anim_zone.height * 1.4)
        img.scale_to_fit_width(self.anim_zone.width * 1.4)
        img.move_to(self.anim_zone.get_center())
        self.play(FadeIn(img, run_time=1.5))
        self._center_group = img  # pour que clear_text puisse la gérer

        chap1 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence01"),
                t("sentence02"),
                t("sentence03"),
            ],
        )
        self.show_chapter(chap1)
        self.wait(3)

        chap2 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence11"),
                t("sentence12"),
                t("sentence13"),
            ],
        )
        self.show_chapter(chap2)
        self.wait(1)

        # --- Vidéo 2 : miroirs dans le train ---
        video1 = FrameSequencePlayer(
            pattern="sortie_frames/frame_*.png",
            fps=60,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width*1.4,
            max_h=self.anim_zone.height*1.4,
            loop=False,
            autoplay=True,
            z=5,
        )
        self.add(video1)
        self.wait(len(video1.files) / video1.fps + 0.2)
       
        self._center_group = Group(img, video1)

        chap3 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence21"),
                t("sentence22"),
                t("sentence23"),
                t("sentence24"),
                {"type": "text", "content":  t("sentence25"), "pause": 0.1},
                {"type": "text", "content":  t("sentence26"), "pause": 3},
                t("sentence27"),

            ],
        )
        self.show_chapter(chap3)
        self.wait(3)

        chap4 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence31"),
                {"type": "text", "content":  t("sentence32"), "pause": 3},
                t("sentence33"),
                t("sentence34"),
                t("sentence35"),
                {"type": "text", "content":  t("sentence36"), "pause": 2},
                t("sentence37"),
            ],
        )
        self.show_chapter(chap4)
        
        cta = Text(t("cta_sub"), color=RED).scale(0.5)
        cta.next_to(self._title_current, 0.15*DOWN, buff=0.6)
        cta.set_z_index(10)

        title_group = VGroup(self._title_current, cta)
        self._title_current = title_group


        self.wait(3)
        self.play(FadeIn(cta, shift=DOWN*0.05), run_time=1)
        self.wait(5)

      #  self._center_group = VGroup(ax, x_label, y_label, graph)
        self.clear_text(clear_figure=True)

 
