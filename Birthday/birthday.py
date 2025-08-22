from manim import *
import manim_helper as mh
from birthday_lang import t
from frame_sequence_fit import FrameSequencePlayer
from Birthday_title_card import show_title_card

class ShortsManual(mh.TextChaptersScene):
    def construct(self):
        self.setup_layout()
        
        
        show_title_card(
            self,
            title_text=t("title"),
            formula_tex=("math", r""),
            kepler_path="birthday_cake.png",  # ajuste le chemin si nécessaire
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",      # idem pour ton logo
            hold=1.0)

        
        chap0 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[],
        )
        self.show_chapter(chap0)


        pad = 0.98
        video1 = FrameSequencePlayer(
            "exports/seq_quatuor_numbers/frame_*.png",
            fps=30,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width*pad,
            max_h=self.anim_zone.height*pad,
            loop=False,
            autoplay=False,   # démarre en pause
            z=5,
        )
        

        self.add(video1)

        # Texte explicatif
        chap1 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence01"),
                t("sentence02"),
                t("sentence03"),
                t("sentence04"),
                t("sentence05"),
                {"type": "text", "content":  t("sentence06"), "pause": 2},
            ],
        )
        self.show_chapter(chap1)


        video2 = FrameSequencePlayer(
            pattern="exports/seq_quatuor_numbers/frame_*.png",  # tes PNG exportés
            fps=30,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width*pad,
            max_h=self.anim_zone.height*pad,
            loop=False,
            z=5,
        )
        
        self.add(video2)
        self.wait(len(video2.files) / video2.fps)

        

#
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
        self.wait(1)
        
        
        chap3 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence21"),
                t("sentence22"),
                t("sentence23"),
                t("sentence24"),
                {"type": "text", "content":  t("sentence25"), "pause": 3},
                t("sentence26"),
                t("sentence27"),
            ],
        )
        self.show_chapter(chap3)
        self.wait(2)

        
        group = Group(video1, video2)
        self._center_group = group

        self.clear_text(bottom_and_figure=True)
        cake = ImageMobject("birthday_cake.png").scale(0.5)  # ton fichier image
        cake.set_z_index(5)
        cake.scale_to_fit_width(self.anim_zone.width * 0.8)
        cake.scale_to_fit_height(self.anim_zone.height * 0.8)
        cake.move_to(self.anim_zone.get_center())
        self.play(FadeIn(cake))
        self._center_group = cake

        chap4 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence31"),
                t("sentence32"),
                t("sentence33"),
                {"type": "text", "content":  t("sentence34"), "pause": 2},
                {"type": "text", "content":  t("sentence35"), "pause": 3},
                t("sentence36"),
                {"type": "text", "content":  t("sentence37"), "pause": 1},
                t("sentence38"),

            ],
        )
        self.show_chapter(chap4)
        # CTA
        cta = Text(t("cta_sub"), color=RED).scale(0.5)
        cta.next_to(self._title_current, DOWN, buff=0.6)
        title_group = VGroup(self._title_current, cta)
        self._title_current = title_group


        self.wait(3)
        self.play(FadeIn(cta, shift=DOWN*0.2), run_time=1)
        self.wait(5)

      #  self._center_group = VGroup(ax, x_label, y_label, graph)
        self.clear_text(clear_figure=True)
