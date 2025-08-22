import os

LANG = os.getenv("SHORT_LANG", "FR")  # FR / EN / ES / PT

TEXT = {
    # ----- Common / Title -----
    "title": {
        "FR": "En somme, c’est simple",
        "EN": "In sum, it's simple",
        "ES": "En suma, es sencillo",
        "PT": "Em suma, é simples",
    },

    # ----- Chapter 1: Visual build of squares -----
    "sentence01": {
        "FR": "Bien avant l'invention des mathématiques modernes, les ",
        "EN": "Long before the invention of modern mathematics, ",
        "ES": "Mucho antes de la invención de las matemáticas modernas, ",
        "PT": "Muito antes da invenção da matemática moderna, ",
    },
    "sentence02": {
        "FR": "penseurs grecs ont résolu le problème suivant:",
        "EN": "Greek thinkers solved the following problem:",
        "ES": "los pensadores griegos resolvieron el siguiente problema:",
        "PT": "os pensadores gregos resolveram o seguinte problema:",
    },
    "sentence03": {
        "FR": "quel serait le résultat de l'addition des nombres impairs",
        "EN": "what would be the result of adding the odd numbers",
        "ES": "¿cuál sería el resultado de sumar los números impares",
        "PT": "qual seria o resultado da soma dos números ímpares",
    },
    "sentence04": {
        "FR": r"1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) ?",
        "EN": r"1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) ?",
        "ES": r"1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) ?",
        "PT": r"1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) ?",
    },
    "sentence05": {
        "FR": r"où $(2n - 1)$ est le n-ième nombre impair.",
        "EN": r"where $(2n - 1)$ is the n-th odd number.",
        "ES": r"donde $(2n - 1)$ es el n-ésimo número impar.",
        "PT": r"onde $(2n - 1)$ é o n-ésimo número ímpar.",
    },
    "c1_anim": {
        "FR": {"type": "text","content": "Chaque couche ajoute un nombre impair de carrés.","anim": lambda scene, line: scene._oddsum_layers_anim(n_max=5, gap=0.25, hold=0.5)},
        "EN": {"type": "text","content": "Each layer adds an odd number of squares.","anim": lambda scene, line: scene._oddsum_layers_anim(n_max=5, gap=0.25, hold=0.5)},
        "ES": {"type": "text","content": "Cada capa añade un número impar de cuadrados.","anim": lambda scene, line: scene._oddsum_layers_anim(n_max=5, gap=0.25, hold=0.5)},
        "PT": {"type": "text","content": "Cada camada adiciona um número ímpar de quadrados.","anim": lambda scene, line: scene._oddsum_layers_anim(n_max=5, gap=0.25, hold=0.5)},
    },

    "sentence11": {
        "FR": "Les Grecs ont utilisé une approche géométrique.",
        "EN": "The Greeks used a geometric approach.",
        "ES": "Los griegos usaron un enfoque geométrico.",
        "PT": "Os gregos usaram uma abordagem geométrica.",
    },
    "sentence12": {
        "FR": "Plutôt que de penser en termes d’addition de nombres,",
        "EN": "Rather than thinking in terms of adding numbers,",
        "ES": "En lugar de pensar en términos de sumar números,",
        "PT": "Em vez de pensar em termos de somar números,",
    },
    "sentence13": {
        "FR": {"type": "text", "content": "ils représentaient chaque unité par un petit carré."},
        "EN": {"type": "text", "content": "they represented each unit with a small square."},
        "ES": {"type": "text", "content": "representaban cada unidad con un pequeño cuadrado."},
        "PT": {"type": "text", "content": "representavam cada unidade por um quadrado."},
    },
    "sentence14": {
        "FR": {"type": "text", "content": r"En ajoutant 3 carrés à un carré, on obtient $4 = 2^{2}$ carrés."},
        "EN": {"type": "text", "content": r"By adding 3 squares to 1 square, we get $4 = 2^{2}$ squares."},
        "ES": {"type": "text", "content": r"Al añadir 3 cuadrados a 1 cuadrado, obtenemos $4 = 2^{2}$."},
        "PT": {"type": "text", "content": r"Somando 3 quadrados a 1, obtemos $4 = 2^{2}$."},
    },
    "sentence15": {
        "FR": {"type": "text", "content": "Puis en ajoutant 5 carrés, on obtient $9 = 3^{2}$ carrés."},
        "EN": {"type": "text", "content": "Then by adding 5 squares, we get $9 = 3^{2}$ squares."},
        "ES": {"type": "text", "content": "Luego, al añadir 5 cuadrados, obtenemos $9 = 3^{2}$."},
        "PT": {"type": "text", "content": "Ao adicionar 5 quadrados, obtemos $9 = 3^{2}$."},
    },
    "sentence16": {
        "FR": "Et ainsi de suite...",
        "EN": "And so on...",
        "ES": "Y así sucesivamente...",
        "PT": "E assim por diante...",
    },
    "sentence17": {
        "FR": r"La somme des $n$ premiers nombres impairs est donc :",
        "EN": r"The sum of the first $n$ odd numbers is therefore:",
        "ES": r"La suma de los primeros $n$ números impares es entonces:",
        "PT": r"A soma dos primeiros $n$ números ímpares é portanto:",
    },
    "sentence18": {
        "FR": r"$1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) = n^{2}$",
        "EN": r"$1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) = n^{2}$",
        "ES": r"$1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) = n^{2}$",
        "PT": r"$1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) = n^{2}$",
    },
    "sentence21": {
        "FR": "De cette formule,",
        "EN": "From this formula,",
        "ES": "De esta fórmula,",
        "PT": "Desta fórmula,",
    },
    "sentence22": {
        "FR": r"$1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) = n^{2}$",
        "EN": r"$1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) = n^{2}$",
        "ES": r"$1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) = n^{2}$",
        "PT": r"$1 + 3 + 5 + 7 + 9 + \dots + (2n - 1) = n^{2}$",
    },
    "sentence23": {
        "FR": "dérive d’autres résultats célèbres.",
        "EN": "other famous results can be derived.",
        "ES": "se derivan otros resultados famosos.",
        "PT": "derivam-se outros resultados famosos.",
    },
    "sentence24": {
        "FR": r"Ajoutons 1 au $n$ termes du côté gauche :",
        "EN": r"Let’s add 1 to the $n$ terms on the left side:",
        "ES": r"Sumemos 1 a los $n$ términos del lado izquierdo:",
        "PT": r"Adicionemos 1 aos $n$ termos do lado esquerdo:",
    },
    "sentence25": {
        "FR": r"$2 + 4 + 6 + 8 + 10 + \dots + (2n) = n^{2} + n$",
        "EN": r"$2 + 4 + 6 + 8 + 10 + \dots + (2n) = n^{2} + n$",
        "ES": r"$2 + 4 + 6 + 8 + 10 + \dots + (2n) = n^{2} + n$",
        "PT": r"$2 + 4 + 6 + 8 + 10 + \dots + (2n) = n^{2} + n$",
    },
    "sentence26": {
        "FR": "en divisant par 2, on obtient :",
        "EN": "dividing by 2, we obtain:",
        "ES": "dividiendo entre 2, obtenemos:",
        "PT": "dividindo por 2, obtemos:",
    },
    "sentence27": {
        "FR": r"$1 + 2 + 3 + 4 + 5 + \dots + n = \frac{n^{2} + n}{2} = \frac{n(n+1)}{2}.$",
        "EN": r"$1 + 2 + 3 + 4 + 5 + \dots + n = \frac{n^{2} + n}{2} = \frac{n(n+1)}{2}.$",
        "ES": r"$1 + 2 + 3 + 4 + 5 + \dots + n = \frac{n^{2} + n}{2} = \frac{n(n+1)}{2}.$",
        "PT": r"$1 + 2 + 3 + 4 + 5 + \dots + n = \frac{n^{2} + n}{2} = \frac{n(n+1)}{2}.$",
    },
    "sentence28": {
        "FR": "C’est la fameuse formule de Gauss.",
        "EN": "This is the famous Gauss formula.",
        "ES": "Esta es la famosa fórmula de Gauss.",
        "PT": "Esta é a famosa fórmula de Gauss.",
    },
    "sentence29": {
        "FR": "Un calcul élégant de la somme des n premiers entiers.",
        "EN": "An elegant calculation of the sum of the first n integers.",
        "ES": "Un cálculo elegante de la suma de los primeros n enteros.",
        "PT": "Um cálculo elegante da soma dos primeiros n inteiros.",
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
    try:
        return TEXT[key][LANG]
    except KeyError:
        return f"[{key}:{LANG} MISSING]"
