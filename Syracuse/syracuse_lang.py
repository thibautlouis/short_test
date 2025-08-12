import os

LANG = os.getenv("SHORT_LANG", "FR")  # <- drives the language per run

TEXT = {
    # ----- Common / Title -----
    "title": {
        "FR": "La mystérieuse suite de Syracuse",
        "EN": "The Mysterious Collatz Sequence",
        "ES": "La misteriosa secuencia de Collatz",
        "PT": "A misteriosa sequência de Collatz",
    },

    # ----- Chapter 1 -----
    "sentence01": {
        "FR": "Prenez n'importe quel nombre entier positif.",
        "EN": "Take any positive integer.",
        "ES": "Toma cualquier número entero positivo.",
        "PT": "Pegue qualquer número inteiro positivo.",
    },
    "sentence02": {
        "FR": "S'il est pair, divisez-le par 2.",
        "EN": "If it’s even, divide it by 2.",
        "ES": "Si es par, divídelo entre 2.",
        "PT": "Se for par, divida-o por 2.",
    },
    "sentence03": {
        "FR": "S'il est impair, multipliez-le par 3 et ajoutez 1.",
        "EN": "If it’s odd, multiply it by 3 and add 1.",
        "ES": "Si es impar, multiplícalo por 3 y súmale 1.",
        "PT": "Se for ímpar, multiplique-o por 3 e some 1.",
    },
    "sentence04": {
        "FR": "Mathématiquement, on écrit :",
        "EN": "Mathematically, we write:",
        "ES": "Matemáticamente, escribimos:",
        "PT": "Matematicamente, escrevemos:",
    },
    "sentence05": {
        # IMPORTANT : pas de $...$ autour, MathTex les gère
        "FR": ("math", r"u_{n+1}=\begin{cases}\dfrac{u_n}{2} & \text{si } u_n \text{ est pair}\\[4pt] 3u_n+1 & \text{si } u_n \text{ est impair}\end{cases}"),
        "EN": ("math", r"u_{n+1}=\begin{cases}\dfrac{u_n}{2} & \text{if } u_n \text{ is even}\\[4pt] 3u_n+1 & \text{if } u_n \text{ is odd}\end{cases}"),
        "ES": ("math", r"u_{n+1}=\begin{cases}\dfrac{u_n}{2} & \text{si } u_n \text{ es par}\\[4pt] 3u_n+1 & \text{si } u_n \text{ es impar}\end{cases}"),
        "PT": ("math", r"u_{n+1}=\begin{cases}\dfrac{u_n}{2} & \text{se } u_n \text{ for par}\\[4pt] 3u_n+1 & \text{se } u_n \text{ for ímpar}\end{cases}"),
    },
    "sentence06": {
        "FR": r"La conjecture affirme que, peu importe le point de départ,",
        "EN": r"The conjecture states that, no matter the starting number,",
        "ES": r"La conjetura afirma que, sin importar el número inicial,",
        "PT": r"A conjectura afirma que, não importa o número inicial,",
    },
    "sentence07": {
        "FR": r"la suite de nombres finit toujours par arriver à 1.",
        "EN": r"the sequence will always end up at 1.",
        "ES": r"la secuencia siempre terminará en 1.",
        "PT": r"a sequência sempre acabará em 1.",
    },
    "sentence08": {
        # Déclenche l’animation du graphe quand cette ligne est écrite
        "FR": {
            "type": "text",
            "content": "Regardons quelques trajectoires pour différents $u_{0}$",
            "anim": lambda scene, line: scene._syracuse_draw_seq(gap_between=0.35, step_slow=4.0)
        },
        "EN": {
            "type": "text",
            "content": "Let’s look at a few trajectories for different $u_{0}$",
            "anim": lambda scene, line: scene._syracuse_draw_seq(gap_between=0.35, step_slow=4.0)
        },
        "ES": {
            "type": "text",
            "content": "Veamos algunas trayectorias para diferentes $u_{0}$",
            "anim": lambda scene, line: scene._syracuse_draw_seq(gap_between=0.35, step_slow=4.0)
        },
        "PT": {
            "type": "text",
            "content": "Vamos ver algumas trajetórias para diferentes $u_{0}$",
            "anim": lambda scene, line: scene._syracuse_draw_seq(gap_between=0.35, step_slow=4.0)
        },
    },

    # ----- Chapter 2 -----
    "sentence11": {
        "FR": "Malgré sa simplicité, personne n’a prouvé la conjecture.",
        "EN": "Despite its simplicity, no one has proved the conjecture.",
        "ES": "Pese a su sencillez, nadie ha probado la conjetura.",
        "PT": "Apesar de sua simplicidade, ninguém provou a conjectura.",
    },
    "sentence12": {
        "FR": "Paul Erdős, grand mathématicien, déclarait",
        "EN": "Paul Erdős, a great mathematician, said",
        "ES": "Paul Erdős, un gran matemático, dijo",
        "PT": "Paul Erdős, um grande matemático, disse",
    },
    "sentence13": {
        "FR": {
            "type": "text",
            "content": "Les mathématiques ne sont pas prêtes pour ce problème. ",
            "color": "#FFD166",
            "scale": 0.55
        },
        "EN": {
            "type": "text",
            "content": "Mathematics is not ready for this problem.",
            "color": "#FFD166",
            "scale": 0.55
        },
        "ES": {
            "type": "text",
            "content": "Las matemáticas no están listas para este problema.",
            "color": "#FFD166",
            "scale": 0.55
        },
        "PT": {
            "type": "text",
            "content": "A matemática não está pronta para este problema.",
            "color": "#FFD166",
            "scale": 0.55
        },
    },
    "sentence14": {
        "FR": "Aujourd’hui, on a vérifié par ordinateur la conjecture",
        "EN": "Today, computers have checked the conjecture",
        "ES": "Hoy, las computadoras han comprobado la conjetura",
        "PT": "Hoje, computadores verificaram a conjectura",
    },
    "sentence15": {
        "FR": r"pour tous les nombres entiers inférieurs à $2{,}36 \times 10^{21}$.",
        "EN": r"for all integers less than $2.36 \times 10^{21}$.",
        "ES": r"para todos los números enteros menores que $2.36 \times 10^{21}$.",
        "PT": r"para todos os números inteiros menores que $2.36 \times 10^{21}$.",
    },
    "sentence16": {
        "FR": "Certains chercheurs se demandent même",
        "EN": "Some researchers even wonder",
        "ES": "Algunos investigadores incluso se preguntan",
        "PT": "Alguns pesquisadores até se perguntam",
    },
    "sentence17": {
        "FR": "si la conjecture de Syracuse pourrait être indécidable.",
        "EN": "if the Collatz conjecture could be undecidable.",
        "ES": "si la conjetura de Collatz podría ser indecidible.",
        "PT": "se a conjectura de Collatz poderia ser indecidível.",
    },
    "sentence18": {
        "FR": "Le mystère de Syracuse reste donc entier.",
        "EN": "The Collatz mystery remains unsolved.",
        "ES": "El misterio de Collatz sigue sin resolverse.",
        "PT": "O mistério de Collatz permanece sem solução.",
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
