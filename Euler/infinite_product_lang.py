import os

LANG = os.getenv("SHORT_LANG", "FR")  # <- drives the language per run

TEXT = {
    # ----- Common / Title -----
    "title": {
        "FR": "Euler : produit infini",
        "EN": "Euler: Infinite Product",
        "ES": "Euler: Producto infinito",
        "PT": "Euler: Produto infinito",
    },

    # ----- Chapter 1 -----
    "preamble": {
        "FR": r"Si un polyn\^ome $P(x)$ a des racines $x_i \neq 0$, alors ",
        "EN": r"If a polynomial $P(x)$ has roots $x_i \neq 0$, then ",
        "ES": r"Si un polinomio $P(x)$ tiene raíces $x_i \neq 0$, entonces ",
        "PT": r"Se um polinômio $P(x)$ tem raízes $x_i \neq 0$, então ",
    },
    "poly_fact": {
        "FR": r"P(x) = \mathrm{Cst} \times \prod_i\!\left(1-\frac{x}{x_i}\right).",
        "EN": r"P(x) = \mathrm{Cst} \times \prod_i\!\left(1-\frac{x}{x_i}\right).",
        "ES": r"P(x) = \mathrm{Cst} \times \prod_i\!\left(1-\frac{x}{x_i}\right).",
        "PT": r"P(x) = \mathrm{Cst} \times \prod_i\!\left(1-\frac{x}{x_i}\right).",
    },
    "ex1": {
        "FR": r"Par exemple: $P(x) = x^{2}-5x+6$,",
        "EN": r"For example: $P(x) = x^{2}-5x+6$,",
        "ES": r"Por ejemplo: $P(x) = x^{2}-5x+6$,",
        "PT": r"Por exemplo: $P(x) = x^{2}-5x+6$,",
    },
    "ex2": {
        "FR": r" peut s'écrire $P(x)= 6(1-x/2)(1-x/3).$",
        "EN": r" can be written as $P(x)= 6(1-x/2)(1-x/3).$",
        "ES": r" se puede escribir como $P(x)= 6(1-x/2)(1-x/3).$",
        "PT": r" pode ser escrito como $P(x)= 6(1-x/2)(1-x/3).$",
    },

    # ----- Chapter 2 -----
    "euler_hook": {
        "FR": "Intuition géniale d'Euler :",
        "EN": "Euler’s brilliant idea:",
        "ES": "La idea brillante de Euler:",
        "PT": "A ideia brilhante de Euler:",
    },
    "treat_poly": {
        "FR": r"Traiter $\sin x$ comme un polynôme à zéros connus.",
        "EN": r"Treat $\sin x$ just like a polynomial with known zeros.",
        "ES": r"Tratar $\sin x$ como un polinomio con ceros conocidos.",
        "PT": r"Tratar $\sin x$ como um polinômio com zeros conhecidos.",
    },
    "sin_zeros": {
        "FR": r"Les racines de $\sin x$ sont $0,\ \pm\pi,\ \pm 2\pi,\ \pm 3\pi,\dots$",
        "EN": r"The zeros of $\sin x$ are $0,\ \pm\pi,\ \pm 2\pi,\ \pm 3\pi,\dots$",
        "ES": r"Las raíces de $\sin x$ son $0,\ \pm\pi,\ \pm 2\pi,\ \pm 3\pi,\dots$",
        "PT": r"As raízes de $\sin x$ são $0,\ \pm\pi,\ \pm 2\pi,\ \pm 3\pi,\dots$",
    },
    "so_write": {
        "FR": "On peut donc écrire :",
        "EN": "So we can write it as:",
        "ES": "Entonces podemos escribirlo como:",
        "PT": "Podemos escrevê-lo como:",
    },
    "sin_prod_1": {
        "FR": r"\sin x = \mathrm{Cst} \times x(1-\frac{x}{\pi})(1+\frac{x}{\pi})(1-\frac{x}{2\pi})(x+\frac{x}{2\pi})\cdots",
        "EN": r"\sin x = \mathrm{Cst} \times x(1-\frac{x}{\pi})(1+\frac{x}{\pi})(1-\frac{x}{2\pi})(1+\frac{x}{2\pi})\cdots",
        "ES": r"\sin x = \mathrm{Cst} \times x(1-\frac{x}{\pi})(1+\frac{x}{\pi})(1-\frac{x}{2\pi})(1+\frac{x}{2\pi})\cdots",
        "PT": r"\sin x = \mathrm{Cst} \times x(1-\frac{x}{\pi})(1+\frac{x}{\pi})(1-\frac{x}{2\pi})(1+\frac{x}{2\pi})\cdots",
    },
    "each_factor": {
        "FR": r"Chaque facteur correspond à un zéro de sin(x).",
        "EN": r"Each factor matches one zero of sin(x).",
        "ES": r"Cada factor corresponde a un cero de sin(x).",
        "PT": r"Cada fator corresponde a um zero de sin(x).",
    },
    "pairing": {
        "FR": r"En factorisant, on regroupe les paires $\pm n\pi$ :",
        "EN": r"Pairing up the $\pm n\pi$ terms gives:",
        "ES": r"Agrupando los términos $\pm n\pi$ obtenemos:",
        "PT": r"Ao agrupar os termos $\pm n\pi$, obtemos:",
    },
    "sin_prod_2": {
        "FR": r"\sin x = \mathrm{Cst} \times x(1-\frac{x^{2}}{\pi^{2}})(1-\frac{x^{2}}{2^{2}\pi^{2}})(1-\frac{x^{2}}{3^{2}\pi^{2}})\cdots",
        "EN": r"\sin x = \mathrm{Cst} \times x(1-\frac{x^{2}}{\pi^{2}})(1-\frac{x^{2}}{2^{2}\pi^{2}})(1-\frac{x^{2}}{3^{2}\pi^{2}})\cdots",
        "ES": r"\sin x = \mathrm{Cst} \times x(1-\frac{x^{2}}{\pi^{2}})(1-\frac{x^{2}}{2^{2}\pi^{2}})(1-\frac{x^{2}}{3^{2}\pi^{2}})\cdots",
        "PT": r"\sin x = \mathrm{Cst} \times x(1-\frac{x^{2}}{\pi^{2}})(1-\frac{x^{2}}{2^{2}\pi^{2}})(1-\frac{x^{2}}{3^{2}\pi^{2}})\cdots",
    },
    "const_one": {
        "FR": r"\lim_{x \to 0} \frac{\sin x}{x} = 1 \quad\Rightarrow\quad  \mathrm{Cst} = 1",
        "EN": r"\lim_{x \to 0} \frac{\sin x}{x} = 1 \quad\Rightarrow\quad  \mathrm{Cst} = 1",
        "ES": r"\lim_{x \to 0} \frac{\sin x}{x} = 1 \quad\Rightarrow\quad  \mathrm{Cst} = 1",
        "PT": r"\lim_{x \to 0} \frac{\sin x}{x} = 1 \quad\Rightarrow\quad  \mathrm{Cst} = 1",
    },
    "final_prod": {
        "FR": r"\sin x = \,x\prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)",
        "EN": r"\sin x = x\prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)",
        "ES": r"\sin x = x\prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)",
        "PT": r"\sin x = x\prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)",
    },
    "cta_sub": {
        "FR": "Explorez plus de maths et de physique — abonnez-vous !",
        "EN": "Explore more math and physics — subscribe!",
        "ES": "Explora más matemáticas y física — ¡suscríbete!",
        "PT": "Explore mais matemática e física — inscreva-se!",
    },
}

def t(key: str) -> str:
    """Return the string for the current language, or a clear placeholder if missing."""
    try:
        return TEXT[key][LANG]
    except KeyError:
        return f"[{key}:{LANG} MISSING]"
