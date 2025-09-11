# -*- coding: utf-8 -*-
from manim import *
import manim_helper as mh
from frame_sequence_fit import FrameSequencePlayer
from doppler_lang import t
from manim import Tex, MathTex, TexTemplate
from doppler_title_card import show_title_card

# ---------------- LaTeX ----------------
tex = TexTemplate()
tex.add_to_preamble(r"\usepackage{amsmath}")
tex.add_to_preamble(r"\usepackage{xcolor}")
Tex.set_default(tex_template=tex)
MathTex.set_default(tex_template=tex)

# ---------------- SCENE ----------------
class ShortsDoppler(mh.TextChaptersScene):
    def construct(self):
        self.setup_layout()
        
        
        show_title_card(
            self,
            title_text=t("title"),
            formula_tex=("math", r""),
            kepler_path="frame_title.png",
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
            hold=1)



        pad = 0.98

        chap0 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[],
        )
        self.show_chapter(chap0)
        
        img = ImageMobject("export_frames_static/frame_00000.png") # ton image
        center=self.anim_zone.get_center(),
        max_w=self.anim_zone.width * 1.2,
        max_h=self.anim_zone.height *  1.2,

        s = min(max_w / img.width, max_h / img.height)
        img = img.scale(s)
        img.set_z_index(5)
        img.move_to(self.anim_zone.get_center())
        self.play(FadeIn(img, run_time=1.0))
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

        # ---------- VIDEO 1 ----------
        video1 = FrameSequencePlayer(
            pattern="export_frames_static/frame_*.png",
            fps=20,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width *  1.2,
            max_h=self.anim_zone.height *  1.2,
            loop=False,
            autoplay=False,
            z=5,
        )
        self.add(video1)
        t0 = self.time

        def sync1(mobj, dt):
            mobj.goto_time(self.time - t0)

        video1.add_updater(sync1)

        dur_vid1 = (len(video1.files) / video1.fps) if video1.files else 0.0
        self.wait(dur_vid1 + 0.05)
        video1.remove_updater(sync1)
        
        
        video2 = FrameSequencePlayer(
            pattern="export_frames/frame_*.png",
            fps=20,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width *  1.2,
            max_h=self.anim_zone.height *  1.2,
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
            ],
        )
        self.show_chapter(chap2)

        # ---------- VIDEO 2 ----------
        video3 = FrameSequencePlayer(
            pattern="export_frames/frame_*.png",
            fps=20,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width *  1.2,
            max_h=self.anim_zone.height *  1.2,
            loop=False,
            autoplay=False,
            z=5,
        )
        self.add(video3)
        t0 = self.time


        video3.add_updater(sync1)

        dur_vid3 = (len(video3.files) / video3.fps) if video3.files else 0.0
        self.wait(dur_vid3 + 0.05)
        video3.remove_updater(sync1)
        
        
        chap3 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence21"),
                t("sentence22"),
                t("sentence23"),
            ],
        )
        self.show_chapter(chap3)




        self._center_group = Group(img, video1, video2, video3)

        self.clear_text(bottom_and_figure=True)
        
        # ---------- VIDEO 2 ----------
        img = ImageMobject("export_frames_galaxy/frame_00000.png") # ton image
        center=self.anim_zone.get_center(),
        max_w=self.anim_zone.width * pad,
        max_h=self.anim_zone.height * pad,

        s = min(max_w / img.width, max_h / img.height)
        img = img.scale(s)
        img.set_z_index(5)
        img.move_to(self.anim_zone.get_center())
        self.play(FadeIn(img, run_time=1.0))
        self._center_group = img  # pour que clear_text puisse la gérer



        
        chap3 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence31"),
                t("sentence32"),
                t("sentence33"),
                t("sentence34"),
                t("sentence35"),
                t("sentence36"),
            ],
        )
        self.show_chapter(chap3)

        
        
        t0 = self.time
        video4 = FrameSequencePlayer(
            pattern="export_frames_galaxy/frame_*.png",
            fps=40,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width * pad,
            max_h=self.anim_zone.height * pad,
            loop=False,
            autoplay=False,
            z=5,
        )
        self.add(video4)


        video4.add_updater(sync1)

        dur_vid4 = (len(video4.files) / video4.fps) if video4.files else 0.0
        self.wait(dur_vid4 + 0.05)
        video4.remove_updater(sync1)
        
        
        chap4 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence41"),
                t("sentence42"),
                t("sentence43"),
                t("sentence44"),
                t("sentence45"),
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

        self._center_group = Group(img, video4)

        self.clear_text(clear_figure=True)
