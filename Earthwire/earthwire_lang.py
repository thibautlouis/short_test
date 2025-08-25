import os

LANG = os.getenv("SHORT_LANG", "FR")  # FR par défaut

TEXT = {
    # ----- Titre -----
    "title": {
        "FR": "La corde autour du monde",
        "EN": "The Rope Around the World",
        "ES": "La cuerda alrededor del mundo",
        "PT": "A corda ao redor do mundo",
    },

    # ----- Intro -----
    "sentence01": {
        "FR": r"Imaginons le problème suivant :",
        "EN": r"Let’s imagine the following problem:",
        "ES": r"Imaginemos el siguiente problema:",
        "PT": r"Vamos imaginar o seguinte problema:",
    },
    "sentence02": {
        "FR": r"quelle longueur de corde faudrait-il pour entourer",
        "EN": r"how long would a rope need to be to go around",
        "ES": r"¿qué longitud de cuerda haría falta para rodear",
        "PT": r"qual o comprimento de corda para dar a volta",
    },
    "sentence03": {
        "FR": r"la Terre d’un pôle à l’autre ?",
        "EN": r"the Earth from pole to pole?",
        "ES": r"la Tierra de un polo al otro?",
        "PT": r"a Terra de um polo ao outro?",
    },

    # ----- Réponse simple -----
    "sentence11": {
        "FR": r"La réponse est immédiate : le rayon de la Terre vaut",
        "EN": r"The answer is immediate: the Earth’s radius is",
        "ES": r"La respuesta es inmediata: el radio de la Tierra es",
        "PT": r"A resposta é imediata: o raio da Terra é",
    },
    "sentence12": {
        "FR": r"6 378 km, donc sa circonférence est",
        "EN": r"6,378 km, so its circumference is",
        "ES": r"6 378 km, por lo tanto su circunferencia es",
        "PT": r"6 378 km, portanto a sua circunferência é",
    },
    "sentence13": {
        "FR": r"$C = 2\pi r \approx 40\,075$ km.",
        "EN": r"$C = 2\pi r \approx 40,075$ km.",
        "ES": r"$C = 2\pi r \approx 40\,075$ km.",
        "PT": r"$C = 2\pi r \approx 40\,075$ km.",
    },
    "sentence14": {
        "FR": r"C’est la longueur de corde qu’il nous faut !",
        "EN": r"That’s the length of rope we’d need!",
        "ES": r"¡Esa es la longitud de cuerda que necesitamos!",
        "PT": r"Essa é a extensão de corda de que precisamos!",
    },

    # ----- Question plus subtile -----
    "sentence15": {
        "FR": r"Mais posons une question moins triviale :",
        "EN": r"But let’s ask a less trivial question:",
        "ES": r"Pero hagamos una pregunta menos trivial:",
        "PT": r"Mas vamos fazer uma pergunta menos trivial:",
    },
    "sentence16": {
        "FR": r"de combien doit-on rallonger cette corde",
        "EN": r"by how much should we lengthen this rope",
        "ES": r"¿cuánto deberíamos alargar esta cuerda",
        "PT": r"quanto devemos aumentar essa corda",
    },
    "sentence17": {
        "FR": r"si on veut qu’elle décolle d’un mètre",
        "EN": r"if we want it to lift by one meter",
        "ES": r"si queremos que se eleve un metro",
        "PT": r"se quisermos que ela se eleve um metro",
    },
    "sentence18": {
        "FR": r"au-dessus du sol, tout autour de la Terre ?",
        "EN": r"above the ground, all around the Earth?",
        "ES": r"sobre el suelo, alrededor de toda la Tierra?",
        "PT": r"acima do solo, em toda a volta da Terra?",
    },

    # ----- Calcul -----
    "sentence21": {
        "FR": r"Notons $C'$ la nouvelle circonférence du cercle",
        "EN": r"Let’s call $C'$ the new circumference of the circle",
        "ES": r"Llamemos $C'$ a la nueva circunferencia del círculo",
        "PT": r"Vamos chamar $C'$ a nova circunferência do círculo",
    },
    "sentence22": {
        "FR": r"autour de la Terre. $C' = 2\pi r'$ où $r' = r + 1\,\text{m}$.",
        "EN": r"around the Earth. $C' = 2\pi r'$, with $r' = r + 1\,\text{m}$.",
        "ES": r"alrededor de la Tierra. $C' = 2\pi r'$, con $r' = r + 1\,\text{m}$.",
        "PT": r"ao redor da Terra. $C' = 2\pi r'$, com $r' = r + 1\,\text{m}$.",
    },
    "sentence23": {
        "FR": r"On veut la différence $L = C' - C$: la longueur",
        "EN": r"We want the difference $L = C' - C$: the length",
        "ES": r"Queremos la diferencia $L = C' - C$: la longitud",
        "PT": r"Queremos a diferença $L = C' - C$: o comprimento",
    },
    "sentence24": {
        "FR": r"supplémentaire pour que la corde décolle d’un mètre.",
        "EN": r"that must be added for the rope to lift by one meter.",
        "ES": r"adicional para que la cuerda se eleve un metro.",
        "PT": r"adicional para que a corda se eleve um metro.",
    },
    "sentence25": {
        "FR": r"empty",
        "EN": r"empty",
        "ES": r"empty",
        "PT": r"empty",
    },
    "sentence26": {
        "FR": r"$L = C' - C = 2\pi(r' - r) = 2\pi \times 1\,\text{m} \approx 6,3\,\text{m}$",
        "EN": r"$L = C' - C = 2\pi(r' - r) = 2\pi \times 1\,\text{m} \approx 6.3\,\text{m}$",
        "ES": r"$L = C' - C = 2\pi(r' - r) = 2\pi \times 1\,\text{m} \approx 6,3\,\text{m}$",
        "PT": r"$L = C' - C = 2\pi(r' - r) = 2\pi \times 1\,\text{m} \approx 6,3\,\text{m}$",
    },
    "sentence27": {
        "FR": r"Il suffit donc d’allonger la corde d’environ 6,3 mètres",
        "EN": r"So you only need to lengthen the rope by about 6.3 m",
        "ES": r"Así que solo hace falta alargar la cuerda unos 6,3 metros",
        "PT": r"Portanto, basta aumentar a corda em cerca de 6,3 metros",
    },
    "sentence28": {
        "FR": r"pour qu’elle décolle d’un mètre tout autour du globe !",
        "EN": r"to make it lift by one meter all around the globe!",
        "ES": r"para que se eleve un metro alrededor de todo el globo!",
        "PT": r"para que ela se eleve um metro em toda a volta do globo!",
    },

    # ----- Explication -----
    "sentence31": {
        "FR": r"La clé du calcul vient du fait que le rayon initial",
        "EN": r"The key to the calculation is that the original radius",
        "ES": r"La clave del cálculo es que el radio inicial",
        "PT": r"A chave do cálculo é que o raio inicial",
    },
    "sentence32": {
        "FR": r"de l’objet disparaît de l’équation.",
        "EN": r"of the object disappears from the equation.",
        "ES": r"del objeto desaparece de la ecuación.",
        "PT": r"do objeto desaparece da equação.",
    },
    "sentence33": {
        "FR": r"Que ce soit autour d’une bille ou autour de la plus",
        "EN": r"Whether it’s around a marble or around the",
        "ES": r"Ya sea alrededor de una canica o alrededor de la",
        "PT": r"Seja ao redor de uma bolinha de gude ou da",
    },
    "sentence34": {
        "FR": r"grande étoile de la galaxie, il faut rallonger",
        "EN": r"largest star in the galaxy, you always need to add",
        "ES": r"estrella más grande de la galaxia, siempre hay que añadir",
        "PT": r"maior estrela da galáxia, sempre é preciso acrescentar",
    },
    "sentence35": {
        "FR": r"la corde de 6,3 mètres pour la faire décoller d’un mètre.",
        "EN": r"6.3 meters of rope to make it rise by one meter.",
        "ES": r"6,3 metros de cuerda para que se eleve un metro.",
        "PT": r"6,3 metros de corda para fazê-la subir um metro.",
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
    try:
        return TEXT[key][LANG]
    except KeyError:
        return f"[{key}:{LANG} MISSING]"

def t(key: str):
    try:
        return TEXT[key][LANG]
    except KeyError:
        return f"[{key}:{LANG} MISSING]"
