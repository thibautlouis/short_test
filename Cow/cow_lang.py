# cow_lang.py
import os

LANG = os.getenv("SHORT_LANG", "FR")  # FR par défaut

TEXT = {
    # ----- Titre -----
    "title": {
        "FR": "Mathématiques Paysannes",
        "EN": "Peasant Math",
        "ES": "Matemáticas Campesinas",
        "PT": "Matemática Camponesa",
    },

    # ----- Intro -----
    "sentence01": {
        "FR": "Imaginons le problème suivant.",
        "EN": "Picture this problem.",
        "ES": "Imagina este problema.",
        "PT": "Imagine este problema.",
    },
    "sentence02": {
        "FR": "Un paysan a quatre poteaux et 110 mètres de clôture.",
        "EN": "A farmer has four posts and 110 meters of fence.",
        "ES": "Un campesino tiene cuatro postes y 110 metros de cerca.",
        "PT": "Um camponês tem quatro postes e 110 metros de cerca.",
    },
    "sentence03": {
        "FR": "Quelle forme d’enclos donne le plus grand pâturage ?",
        "EN": "What shape of pen gives the biggest field?",
        "ES": "¿Qué forma de corral da el mayor campo?",
        "PT": "Qual formato de cercado dá o maior pasto?",
    },
    
    # ----- Chapitre 1 : mise en équation -----
    "sentence11": {
        "FR": "Appelons x et y les côtés de l'enclos.",
        "EN": "Call the sides of the pen x and y.",
        "ES": "Llamemos x e y a los lados del corral.",
        "PT": "Chamemos x e y os lados do cercado.",
    },
    "sentence12": {
        "FR": r"Son périmètre fait 110 mètres :  $P = 2x + 2y = 110 \,\text{m}$ ",
        "EN": r"Its perimeter is 110 meters: $P = 2x + 2y = 110 \,\text{m}$ ",
        "ES": r"Su perímetro es 110 metros: $P = 2x + 2y = 110 \,\text{m}$ ",
        "PT": r"Seu perímetro é 110 metros: $P = 2x + 2y = 110 \,\text{m}$ ",
    },
    "sentence13": {
        "FR": r"et son aire est donnée par : $A(x,y) = x y$.",
        "EN": r"and its area is: $A(x,y) = x y.$",
        "ES": r"y su área es: $A(x,y) = x y.$",
        "PT": r"e sua área é: $A(x,y) = x y.$",
    },

    # ----- Chapitre 2 : pourquoi un Lagrangien ? -----
    "sentence21": {
        "FR": r"Nous voulons maximiser $A(x,y)$.",
        "EN": r"We want to maximize $A(x,y).$",
        "ES": r"Queremos maximizar $A(x,y).$",
        "PT": r"Queremos maximizar $A(x,y).$",
    },
    "sentence22": {
        "FR": "Mais x et y ne sont pas libres : ils doivent respecter",
        "EN": "But x and y aren’t free: they must satisfy",
        "ES": "Pero x e y no son libres: deben respetar",
        "PT": "Mas x e y não são livres: devem respeitar",
    },
    "sentence23": {
        "FR": "la contrainte du périmètre.",
        "EN": "the perimeter constraint.",
        "ES": "la restricción del perímetro. ",
        "PT": "a restrição do perímetro.",
    },
    "sentence24": {
        "FR": "La méthode de Lagrange combine objectif et contrainte",
        "EN": "Lagrange’s method mixes goal and constraint ",
        "ES": "El método de Lagrange combina objetivo y restricción ",
        "PT": "O método de Lagrange combina objetivo e restrição ",
    },
    "sentence25": {
        "FR": "dans une seule fonction:",
        "EN": "in a single function:",
        "ES": "en una sola función:",
        "PT": "em uma única função:",
    },
    "sentence26": {
        "FR": r"""$
    \begin{array}{rcl}
    L(x,y,\lambda) &=& A(x,y)-\lambda\,[P(x,y)-110]\\
                &=& x y - \lambda\,(2x+2y-110)
    \end{array}$
    """,
        "EN": r"""$
    \begin{array}{rcl}
    L(x,y,\lambda) &=& A(x,y)-\lambda\,[P(x,y)-110]\\
                &=& x y - \lambda\,(2x+2y-110)
    \end{array}$
    """,
        "ES": r"""$
    \begin{array}{rcl}
    L(x,y,\lambda) &=& A(x,y)-\lambda\,[P(x,y)-110]\\
                &=& x y - \lambda\,(2x+2y-110)
    \end{array}$
    """,
        "PT": r"""$
    \begin{array}{rcl}
    L(x,y,\lambda) &=& A(x,y)-\lambda\,[P(x,y)-110]\\
                &=& x y - \lambda\,(2x+2y-110)
    \end{array}$
    """,
    },
    "sentence27": {
        "FR": "Maximiser l’aire sous contrainte revient à maximiser L.",
        "EN": "Maximizing the area with constraint means maximizing L.",
        "ES": "Maximizar el área con restricción equivale a maximizar L.",
        "PT": "Maximizar a área com restrição equivale a maximizar L.",
    },
    "sentence31": {
        "FR": "On calcule les dérivées partielles :",
        "EN": "Now we take the partial derivatives:",
        "ES": "Ahora calculamos las derivadas parciales:",
        "PT": "Agora calculamos as derivadas parciais:",
    },
    "sentence32": {
        "FR": r"$\frac{\partial L}{\partial x} = y - 2\lambda = 0, \ \frac{\partial L}{\partial y} = x - 2\lambda = 0$",
        "EN": r"$\frac{\partial L}{\partial x} = y - 2\lambda = 0, \ \frac{\partial L}{\partial y} = x - 2\lambda = 0$",
        "ES": r"$\frac{\partial L}{\partial x} = y - 2\lambda = 0, \ \frac{\partial L}{\partial y} = x - 2\lambda = 0$",
        "PT": r"$\frac{\partial L}{\partial x} = y - 2\lambda = 0, \ \frac{\partial L}{\partial y} = x - 2\lambda = 0$",
    },
    "sentence33": {
        "FR": r"Ces équations impliquent $x = y = 2\lambda$",
        "EN": r"These equations tell us $x = y = 2\lambda$",
        "ES": r"Estas ecuaciones nos dicen $x = y = 2\lambda$",
        "PT": r"Essas equações nos dizem $x = y = 2\lambda$",
    },
    "sentence34": {
        "FR": "La solution optimale est donc un carré.",
        "EN": "So the best shape is a square.",
        "ES": "Así que la mejor forma es un cuadrado.",
        "PT": "Então o melhor formato é um quadrado.",
    },
    "sentence35": {
        "FR": "La longueur d'un des cotés du carré est donnée par:",
        "EN": "One side of the square is:",
        "ES": "Un lado del cuadrado es:",
        "PT": "Um lado do quadrado é:",
    },
    "sentence36": {
        "FR": r"$2x + 2x = 110 \,\text{m} \;\Rightarrow\; x = 27{,}5 \,\text{m}.$",
        "EN": r"$2x + 2x = 110 \,\text{m} \;\Rightarrow\; x = 27{,}5 \,\text{m}.$",
        "ES": r"$2x + 2x = 110 \,\text{m} \;\Rightarrow\; x = 27{,}5 \,\text{m}.$",
        "PT": r"$2x + 2x = 110 \,\text{m} \;\Rightarrow\; x = 27{,}5 \,\text{m}.$",
    },
    "sentence37": {
        "FR": r"et l'aire maximale vaut : $A_{\max} = (27{,}5 \,\text{m})^2 = 756{,}25 \,\text{m}^2$.",
        "EN": r"and the biggest area is: $A_{\max} = (27{,}5 \,\text{m})^2 = 756{,}25 \,\text{m}^2.$",
        "ES": r"y el área máxima es: $A_{\max} = (27{,}5 \,\text{m})^2 = 756{,}25 \,\text{m}^2.$",
        "PT": r"e a área máxima é: $A_{\max} = (27{,}5 \,\text{m})^2 = 756{,}25 \,\text{m}^2.$",
    },
    
    # ----- Call-to-action -----
    "cta_sub": {
        "FR": "Explorez plus de maths et d’astrophysique — abonnez-vous !",
        "EN": "Discover more math and astrophysics — subscribe!",
        "ES": "Descubre más matemáticas y astrofísica — ¡suscríbete!",
        "PT": "Descubra mais matemática e astrofísica — inscreva-se!",
    },
}

def t(key: str):
    try:
        return TEXT[key][LANG]
    except KeyError:
        return f"[{key}:{LANG} MISSING]"
