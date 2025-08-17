
import os

LANG = os.getenv("SHORT_LANG", "FR")  # drive language per run

TEXT = {
    # ----- Common / Title -----
    "title": {
        "FR": "Le centre de l’Univers ?",
        "EN": "The Center of the Universe?",
        "ES": "¿El centro del universo?",
        "PT": "O centro do Universo?",
    },

    # ----- Chapter 1 (2D first) -----
    "sentence01": {
        "FR": "En 1929, Edwin Hubble observe que les galaxies qui nous",
        "EN": "In 1929, Edwin Hubble observed that the galaxies ",
        "ES": "En 1929, Edwin Hubble observó que las galaxias a nuestro",
        "PT": "Em 1929, Edwin Hubble observou que as galáxias ao nosso",
    },
    "sentence02": {
        "FR": "entourent s’éloignent de nous, avec une vitesse",
        "EN": "around us are receding from us, with a speed",
        "ES": "alrededor se alejan de nosotros, con una velocidad",
        "PT": "redor estão se afastando de nós, com uma velocidade",
    },
    "sentence03": {
        "FR": r"proportionnelle à leur distance: $v \propto d$.",
        "EN": r"proportional to their distance: $v \propto d$.",
        "ES": r"proporcional a su distancia: $v \propto d$.",
        "PT": r"proporcional à sua distância: $v \propto d$.",
    },
    "sentence04": {
        "FR": "Plus une galaxie est lointaine, plus elle s’éloigne vite.",
        "EN": "The farther a galaxy is, the faster it recedes.",
        "ES": "Cuanto más lejana es una galaxia, más rápido se aleja.",
        "PT": "Quanto mais distante, mais rápido se afasta.",
    },
    "sentence05": {
        "FR": "Mais si toutes les galaxies s’éloignent de nous",
        "EN": "But if all galaxies move away from us,",
        "ES": "Pero si todas las galaxias se alejan de nosotros,",
        "PT": "Mas se todas as galáxias se afastam de nós,",
    },
    "sentence06": {
        "FR": "cela veut-il dire que nous occupons une place",
        "EN": "does that mean we hold a privileged position",
        "ES": "¿significa eso que ocupamos un lugar",
        "PT": "isso significa que ocupamos um lugar",
    },
    "sentence07": {
        "FR": "privilégiée dans l’Univers ?",
        "EN": "in the Universe?",
        "ES": "privilegiado en el Universo?",
        "PT": "privilegiado no Universo?",
    },

    # ----- Chapter 2 (1D perspective change) -----
    "sentence11": {
        "FR": "Pour répondre à cette question, simplifions le",
        "EN": "To answer this question, let’s simplify the",
        "ES": "Para responder a esta pregunta, simplifiquemos el",
        "PT": "Para responder a esta questão, vamos simplificar o",
    },
    "sentence12": {
        "FR": "problème avec un exemple à une dimension.",
        "EN": "problem with a one-dimensional example.",
        "ES": "problema con un ejemplo unidimensional.",
        "PT": "problema com um exemplo unidimensional.",
    },
    "sentence13": {
        "FR": "Représentons les vitesses proportionnelles à la distance.",
        "EN": "Let’s show velocities proportional to distance.",
        "ES": "Mostremos las velocidades proporcionales a la distancia.",
        "PT": "Mostremos as velocidades proporcionais à distância.",
    },
    "sentence14": {
        "FR": "Si la galaxie la plus proche s’éloigne à la vitesse v,",
        "EN": "If the nearest galaxy recedes at speed v,",
        "ES": "Si la galaxia más cercana se aleja a velocidad v,",
        "PT": "Se a galáxia mais próxima se afasta a velocidade v,",
    },
    "sentence15": {
        "FR": "la suivante s’éloigne à la vitesse 2v.",
        "EN": "the next one recedes at speed 2v.",
        "ES": "la siguiente se aleja a velocidad 2v.",
        "PT": "a seguinte se afasta a velocidade 2v.",
    },
    "sentence16": {
        "FR": "Revenons maintenant à notre point de départ,",
        "EN": "Now let’s return to our starting point,",
        "ES": "Volvamos ahora a nuestro punto de partida,",
        "PT": "Voltemos agora ao nosso ponto de partida,",
    },
    "sentence17": {
        "FR": "et changeons de position de référence.",
        "EN": "and change the reference position.",
        "ES": "y cambiemos de posición de referencia.",
        "PT": "e mudemos a posição de referência.",
    },
    "sentence18": {
        "FR": "Pour cet observateur aussi toutes les galaxies s’éloignent",
        "EN": "For this observer too, all galaxies recede",
        "ES": "Para este observador también, todas las galaxias se alejan",
        "PT": "Para este observador também, todas as galáxias se afastam",
    },
    "sentence19": {
        "FR": "avec une vitesse proportionnelle à leur distance.",
        "EN": "with a speed proportional to their distance.",
        "ES": "con una velocidad proporcional a su distancia.",
        "PT": "com uma velocidade proporcional à sua distância.",
    },

    # ----- Chapter 3 -----
    "sentence21": {
        "FR": "On peut démontrer mathématiquement que la loi $v \propto d$",
        "EN": "One can show mathematically that the law $v \propto d$",
        "ES": "Se puede demostrar matemáticamente que la ley $v \propto d$",
        "PT": "Pode-se demonstrar matematicamente que a lei $v \propto d$",
    },
    "sentence22": {
        "FR": "est la seule possible dans un Univers homogène et isotrope",
        "EN": "is only possible in a homogeneous and isotropic Universe",
        "ES": "es la única posible en un Universo homogéneo e isótropo",
        "PT": "é a única possível em um Universo homogêneo e isotrópico",
    },
    "sentence23": {
        "FR": "c’est-à-dire un Univers qui n’admet pas de centre.",
        "EN": "that is, a Universe with no center.",
        "ES": "es decir, un Universo sin centro.",
        "PT": "ou seja, um Universo sem centro.",
    },
    "sentence24": {
        "FR": "Une loi d’expansion différente indiquerait qu’il existe",
        "EN": "A different expansion law would indicate the existence of",
        "ES": "Una ley de expansión diferente indicaría la existencia de",
        "PT": "Uma lei de expansão diferente indicaria a existência de",
    },
    "sentence25": {
        "FR": "des endroits privilégiés dans l’Univers.",
        "EN": "privileged places in the Universe.",
        "ES": "lugares privilegiados en el Universo.",
        "PT": "lugares privilegiados no Universo.",
    },
    # ----- CTA -----
    "cta_sub": {
        "FR": "Explorez plus de maths et d’astrophysique — abonnez-vous !",
        "EN": "Explore more math & astrophysics — subscribe!",
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
