from manim import *

class LightClockTriangleWithReturn(Scene):
    L_val   = 2.0    # distance entre miroirs
    v_val   = 0.6    # vitesse du train (unités de c si c=1)
    c_val   = 1.0    # vitesse de la lumière
    dt_val  = 4.0    # Δt = durée aller-retour complet
    numeric = False  # True = affiche valeurs numériques

    def construct(self):
        L, v, c, dt = self.L_val, self.v_val, self.c_val, self.dt_val
        dx = v * (dt/2)

        # sommets
        A = np.array([0, 0, 0])      # départ bas
        B = np.array([dx, L, 0])     # haut
        C = np.array([v*dt, 0, 0])   # retour bas
        foot = np.array([dx, 0, 0])  # pied de la verticale

        # segments
        base   = Line(A, foot, color=WHITE, stroke_width=4)
        vert   = Line(foot, B, color=WHITE, stroke_width=4)
        hyp_up = Line(A, B, color=YELLOW, stroke_width=6)
        hyp_down = Line(B, C, color=YELLOW, stroke_width=6)

        # angle droit en pied de la verticale
        right_angle = VGroup(
            Line(foot+0.3*LEFT, foot+0.3*LEFT+0.3*UP),
            Line(foot+0.3*UP,   foot+0.3*LEFT+0.3*UP)
        ).set_stroke(WHITE, 3)

        # --- Animation ---

        # 1) tracer aller AB
        self.play(Create(hyp_up))
        # 2) tracer retour BC
        self.play(Create(hyp_down))

        # 3) afficher sommets
        labA = MathTex("A").scale(0.9).next_to(A, DOWN+LEFT, buff=0.2)
        labB = MathTex("B").scale(0.9).next_to(B, UP+RIGHT, buff=0.2)
        labC = MathTex("C").scale(0.9).next_to(C, DOWN+RIGHT, buff=0.2)
        self.play(Write(labA), Write(labB), Write(labC))

        # 4) tracer côtés blancs + labels
        self.play(Create(base), Create(vert), FadeIn(right_angle))

        if self.numeric:
            lab_base = MathTex(fr"\tfrac{{v\,\Delta t}}{{2}} = {dx:.2f}").scale(0.9).next_to(base, DOWN, buff=0.2)
            lab_vert = MathTex(fr"L = {L:.2f}").scale(0.9).next_to(vert, RIGHT, buff=0.2)
            lab_hyp  = MathTex(fr"\tfrac{{c\,\Delta t}}{{2}} = {c*(dt/2):.2f}").scale(0.9).move_to(hyp_up.get_midpoint()+0.35*UP)
        else:
            lab_base = MathTex(r"\tfrac{v\,\Delta t}{2}").scale(0.9).next_to(base, DOWN, buff=0.2)
            lab_vert = MathTex(r"L").scale(0.9).next_to(vert, RIGHT, buff=0.2)
            lab_hyp  = MathTex(r"\tfrac{c\,\Delta t}{2}").scale(0.9).move_to(hyp_up.get_midpoint()+0.35*UP)

        self.play(Write(lab_base), Write(lab_vert), Write(lab_hyp))

        self.wait(2)
