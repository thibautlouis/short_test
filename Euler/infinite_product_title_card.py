from manim import *
from manim_helper import *
from infinite_product_lang import t

BG = BLACK
GOLD = "#FFD700"
WHITE = "#FFFFFF"

def build_title_card_group(title_text: str,
                           formula_tex: str,
                           logo_path: str | None = "/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png"):

    TITLE_H, CENTER_H, BOTTOM_H = 3.0, 10.6, 2.4
    total = TITLE_H + CENTER_H + BOTTOM_H
    fw = 7.8
    bottom_zone = Rectangle(width=fw, height=BOTTOM_H).set_stroke(opacity=0).move_to([0, -total/2 + BOTTOM_H/2, 0])
    
    title = Tex(title_text).set_color(WHITE)
    title.scale(1.5)
    title.move_to( UP*4)

    formula = MathTex(formula_tex).set_color(GOLD)
    qmarks = Tex("?")
    formula.scale(1.2)
    formula.move_to( UP*1)  # petit décalage vers l’intérieur
    qmarks.scale(2.5)
    qmarks.move_to(RIGHT*3.8 + UP*1.1 )

    group = Group(title, formula, qmarks)

    logo = ImageMobject(logo_path)
    logo.scale(0.2)
    logo.move_to( DOWN*4)  # petit décalage vers l’intérieur
    group.add(logo)

    return group

def show_title_card(scene: Scene,
                    title_text: str,
                    formula_tex: str,
                    logo_path: str,
                    hold: float = 0.7):
    """Add + hold + fade the title card inside an existing Scene."""
    scene.camera.background_color = BG
    group = build_title_card_group(title_text, formula_tex, logo_path)
    scene.add(group)
    scene.wait(hold)
    scene.play(FadeOut(group), run_time=1)


class TitleCard(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        g = build_title_card_group(
            title_text=t("title"),  # ou t("title") si tu veux
            formula_tex=r"\sin x = x \prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)",
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
        )
        self.add(g)
