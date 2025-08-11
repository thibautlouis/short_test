import os

LANG = os.getenv("SHORT_LANG", "FR")  # <- drives the language per run

TEXT = {
    # ----- Common / Title -----
    "title": {
        "FR": "La mystérieuse suite de Syracuse",
        "EN": "",
        "ES": "",
        "PT": "",
    },

    # ----- Chapter 1 -----
    "sentence01": {
        "FR": "Prenez n'importe quel nombre entier positif.",
        "EN": r"",
        "ES": r"",
        "PT": r"",
    },
    "sentence02": {
        "FR": "S'il est pair, divisez-le par 2.",
        "EN": r"",
        "ES": r"",
        "PT": r"",
    },
    "sentence03": {
        "FR": "S'il est impair, multipliez-le par 3 et ajoutez 1.",
        "EN": r"",
        "ES": r"",
        "PT": r"",
    },
    "sentence04": {
        # IMPORTANT : pas de $...$ autour, MathTex les gère
        "FR": ("math", r"u_{n+1}=\begin{cases}\dfrac{u_n}{2} & \text{si } u_n \text{ est pair}\\[4pt] 3u_n+1 & \text{si } u_n \text{ est impair}\end{cases}"),
        "EN": r"",
        "ES": r"",
        "PT": r"",
    },
    "sentence05": {
        "FR": r"La conjecture est que, peu importe le point de départ,",
        "EN": r"",
        "ES": r"",
        "PT": r"",
    },
    "sentence06": {
        "FR": r"la suite de nombre finit toujours par arriver à 1.",
        "EN": r"",
        "ES": r"",
        "PT": r"",
    },
    "sentence07": {
        # Déclenche l’animation du graphe quand cette ligne est écrite
        "FR": {
            "type": "text",
            "content": "Regardons quelques trajectoires pour différent $u_{0}$",
            "anim": lambda scene, line: scene._syracuse_draw_seq(gap_between=0.35, step_slow=4.0)},
        "EN": r"",
        "ES": r"",
        "PT": r"",
    },

    # ----- CTA -----
    "cta_sub": {
        "FR": "Explorez plus de maths et d’astrophysique — abonnez-vous !",
        "EN": "Explore more math and astrophysics — subscribe!",
        "ES": "Explora más matemáticas y astrofísica — ¡suscríbete!",
        "PT": "Explore mais matemática e astrofísica — inscreva-se!",
    },
}

def t(key: str):
    """Return the object for the current language (str / ('math', ...) / dict)."""
    try:
        return TEXT[key][LANG]
    except KeyError:
        return f"[{key}:{LANG} MISSING]"

