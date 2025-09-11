# expansion.py
import manim as mn
import numpy as np
import os

import manim_helper as mh
from imo_lang import t, LANG
from imo_title_card import show_imo_title_card
from manim import Tex, MathTex, TexTemplate

# ---------- Config vidéo (9:16) ----------
mn.config.frame_width  = 9
mn.config.frame_height = 16
mn.config.pixel_width  = 1080
mn.config.pixel_height = 1920
BG  = mn.BLACK

tex = TexTemplate()
tex.add_to_preamble(r"\usepackage{amsmath}")  # utile si tu utilises aligned ailleurs
tex.add_to_preamble(r"\usepackage{xcolor}")   # nécessaire pour \textcolor / \color
Tex.set_default(tex_template=tex)
MathTex.set_default(tex_template=tex)


class ShortsManual(mh.TextChaptersScene):

    # ------------------------
    #         SCÈNE
    # ------------------------
    def construct(self):
        self.camera.background_color = BG
        self.setup_layout()
        
                
        
        show_imo_title_card(
            self,
            title_text=t("title"),
            image_path="money.png",
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
            hold=1)



        chap0 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[],
        )
        self.show_chapter(chap0)
        
        Image = mn.ImageMobject("GPT.png").scale(0.5)  # ton fichier image
        Image.set_z_index(5)
        Image.scale_to_fit_width(self.anim_zone.width * 0.8)
        Image.scale_to_fit_height(self.anim_zone.height * 0.8)
        Image.move_to(self.anim_zone.get_center())
        self.play(mn.FadeIn(Image))
        self._center_group = Image


        chap1 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence01"),
                t("sentence02"),
                t("sentence03"),
                t("sentence04"),
            ],
        )
        self.show_chapter(chap1)
        self.wait(2)

        chap2 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence11"),
                t("sentence12"),
                t("sentence13"),
                t("sentence14"),
                {"type": "text", "content":  t("sentence15"), "pause": 3},
                t("sentence16"),

            ],
        )
        self.show_chapter(chap2)
        self.wait(4)
        self.clear_text(bottom_and_figure=True)

        Image = mn.ImageMobject("money.png").scale(0.5)  # ton fichier image
        Image.set_z_index(5)
        Image.scale_to_fit_width(self.anim_zone.width * 1)
        Image.scale_to_fit_height(self.anim_zone.height * 1)
        Image.move_to(self.anim_zone.get_center())
        self.play(mn.FadeIn(Image))
        self._center_group = Image



        chap3 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence21"),
                t("sentence22"),
                t("sentence23"),
                t("sentence24"),
                t("sentence25"),

            ],
        )
        self.show_chapter(chap3)
        self.wait(5)



        chap4 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence31"),
                {"type": "text", "content":  t("sentence32"), "pause": 3},
                t("sentence33"),
                {"type": "text", "content":  t("sentence34"), "pause": 2},
                t("sentence35"),
            ],
        )
        self.show_chapter(chap4)
        self.wait(4)


        chap5 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence41"),
                {"type": "text", "content":  t("sentence42"), "pause": 3},
                t("sentence43"),
                ("text", t("sentence44"), {"color": (0, 0, 0, 0)}),
                t("sentence45"),
                t("sentence46"),
            ],
        )
        self.show_chapter(chap5)
        self.wait(3)
        
        cta = mn.Text(t("cta_sub"), color= mn.RED).scale(0.5)
        cta.next_to(self._title_current, 0.15* mn.DOWN, buff=0.6)
        cta.set_z_index(10)

        title_group =  mn.VGroup(self._title_current, cta)
        self._title_current = title_group

        self.wait(3)
        self.play( mn.FadeIn(cta, shift= mn.DOWN*0.05), run_time=1)
        self.wait(5)

        self.clear_text(clear_figure=True)
