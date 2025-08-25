
import manim as mn
import manim_helper as mh
from frame_sequence_fit import FrameSequencePlayer  # comme dans birthday.py
from earthwire_lang import t
from earthwire_title_card import show_title_card

mn.config.frame_width  = 9
mn.config.frame_height = 16
mn.config.pixel_width  = 1080
mn.config.pixel_height = 1920

class EarthRopeFromFrames(mh.TextChaptersScene):
    def construct(self):
        self.setup_layout()
        pad = 0.98
        
        show_title_card(
            self,
            title_text=t("title"),
            formula_tex=("math", r""),
            kepler_path="earth_rope.png",  # ajuste le chemin si nécessaire
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",      # idem pour ton logo
            hold=1.0)

               
        chap0 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[],
        )
        self.show_chapter(chap0)


        # 1) Terre seule (image fixe/séquence courte)
        earth_only = FrameSequencePlayer(
            pattern="exports/earth_fade/frame_*.png",
            fps=60,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width*pad,
            max_h=self.anim_zone.height*pad,
            loop=False, autoplay=True, z=5,
        )
        self.add(earth_only)
        self.wait(len(earth_only.files)/earth_only.fps)

        chap1 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence01"),
                t("sentence02"),
                t("sentence03"),
            ],
        )
        self.show_chapter(chap1)
        self.wait(1)


        # 2) Création de la corde (révélation)
        rope_draw = FrameSequencePlayer(
            pattern="exports/rope_draw/frame_*.png",
            fps=60,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width*pad,
            max_h=self.anim_zone.height*pad,
            loop=False, autoplay=True, z=5,
        )
        self.add(rope_draw)
        self.wait(len(rope_draw.files)/rope_draw.fps)
        
        
        chap2 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence11"),
                t("sentence12"),
                {"type": "text", "content":  t("sentence13"), "pause": 2},
                t("sentence14"),
                t("sentence15"),
                t("sentence16"),
                t("sentence17"),
                t("sentence18"),

            ],
        )
        self.show_chapter(chap2)


        # 3) Agrandissement de la corde
        rope_grow = FrameSequencePlayer(
            pattern="exports/rope_grow/frame_*.png",
            fps=60,
            center=self.anim_zone.get_center(),
            max_w=self.anim_zone.width*pad,
            max_h=self.anim_zone.height*pad,
            loop=False, autoplay=True, z=5,
        )
        self.add(rope_grow)
        self.wait(len(rope_grow.files)/rope_grow.fps)


        group = mn.Group(earth_only, rope_draw, rope_grow)
        self._center_group = group

        self.wait(2)

        chap3 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence21"),
                {"type": "text", "content":  t("sentence22"), "pause": 3},
                t("sentence23"),
                {"type": "text", "content":  t("sentence24"), "pause": 3},
                ("text", t("sentence25"), {"color": (0, 0, 0, 0)}),
                {"type": "text", "content":  t("sentence26"), "pause": 3},
                t("sentence27"),
                t("sentence28"),
            ],
        )
        self.show_chapter(chap3)
        self.wait(3)
        
        chap4 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence31"),
                {"type": "text", "content":  t("sentence32"), "pause": 2},
                t("sentence33"),
                t("sentence34"),
                t("sentence35"),
            ],
        )
        self.show_chapter(chap4)
        # CTA
        cta = mn.Text(t("cta_sub"), color=mn.RED).scale(0.5)
        cta.next_to(self._title_current, mn.DOWN, buff=0.6)
        cta.set_z_index(999)  
        title_group = mn.VGroup(self._title_current, cta)
        self._title_current = title_group


        self.wait(3)
        self.play(mn.FadeIn(cta, shift=mn.DOWN*0.2), run_time=1)
        self.wait(5)

      #  self._center_group = VGroup(ax, x_label, y_label, graph)
        self.clear_text(clear_figure=True)
