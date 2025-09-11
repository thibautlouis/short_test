
import os

LANG = os.getenv("SHORT_LANG", "FR")  # drive language per run

TEXT = {
    # ----- Common / Title -----
    "title": {
        "FR": "Mathématiques immobilières",
        "EN": "Real Estate Math",
        "ES": "Matemáticas inmobiliarias",
        "PT": "Matemática imobiliária",
    },

    # ----- Chapitre 1 -----
    "sentence01": {
        "FR": "Imaginons que l’on emprunte 200 000 € à une banque.",
        "EN": "Imagine borrowing £200,000 from a bank.",
        "ES": "Imagina pedir prestados 200 000 € a un banco.",
        "PT": "Imagine pegar 200 000 € emprestados de um banco.",
    },
    "sentence02": {
        "FR": "La banque propose un taux annuel de 3\%, sur 20 ans.",
        "EN": "The bank offers a 3\% annual rate, over 20 years.",
        "ES": "El banco ofrece un interés anual del 3\% a 20 años.",
        "PT": "O banco oferece uma taxa anual de 3\% por 20 anos.",
    },
    "sentence03": {
        "FR": "Quelle sera la mensualité à rembourser ?",
        "EN": "What will the monthly payment be?",
        "ES": "¿Cuál será la cuota mensual a pagar?",
        "PT": "Qual será a prestação mensal?",
    },
    "sentence04": {
        "FR": "Et quel sera le coût total du prêt ?",
        "EN": "And what will the total cost of the loan be?",
        "ES": "¿Y cuál será el costo total del préstamo?",
        "PT": "E qual será o custo total do empréstimo?",
    },

    # ----- Chapitre 2 -----
    "sentence11": {
        "FR": "La clé du calcul est le concept de valeur actuelle.",
        "EN": "The key idea is the concept of present value.",
        "ES": "La clave del cálculo es el concepto de valor presente.",
        "PT": "A chave do cálculo é o conceito de valor presente.",
    },
    "sentence12": {
        "FR": "C’est la valeur de l’argent au moment du prêt.",
        "EN": "It’s the value of money at the time of the loan.",
        "ES": "Es el valor del dinero en el momento del préstamo.",
        "PT": "É o valor do dinheiro no momento do empréstimo.",
    },
    "sentence13": {
        "FR": "En valeur actuelle, la valeur de la mensualité baisse.",
        "EN": "In present value terms, each payment is worth less \& less.",
        "ES": "En valor presente, cada cuota vale cada vez menos.",
        "PT": "Em valor presente, cada prestação vale cada vez menos.",
    },
    "sentence14": {
        "FR": r"Une mensualité $M$ payée le $1^{\rm er}$ mois vaut $\dfrac{M}{1+i}$.",
        "EN": r"A payment $M$ made in the first month is worth $\dfrac{M}{1+i}$.",
        "ES": r"Una cuota $M$ pagada el primer mes vale $\dfrac{M}{1+i}$.",
        "PT": r"Uma prestação $M$ paga no primeiro mês vale $\dfrac{M}{1+i}$.",
    },
    "sentence15": {
        "FR": r"Où $i$ est le taux mensuel : $i = \dfrac{\text{taux annuel}}{12} = 0{,}25\%$.",
        "EN": r"Where $i$ is the monthly rate: $i = \dfrac{\text{annual rate}}{12} = 0.25\%$.",
        "ES": r"Donde $i$ es la tasa mensual: $i = \dfrac{\text{tasa anual}}{12} = 0,25\%$.",
        "PT": r"Onde $i$ é a taxa mensal: $i = \dfrac{\text{taxa anual}}{12} = 0,25\%$.",
    },
    "sentence16": {
        "FR": r"Au $24^{\text{e}}$ mois, elle vaudra $\dfrac{M}{(1+i)^{24}} = 0.94 \ $M.",
        "EN": r"By the 24th month, it will be worth $\dfrac{M}{(1+i)^{24}} = 0.94 \ $M.",
        "ES": r"En el 24º mes, valdrá $\dfrac{M}{(1+i)^{24}} = 0.94 \ $M.",
        "PT": r"No 24º mês, valerá $\dfrac{M}{(1+i)^{24}} = 0.94 \ $M.",
    },

    # ----- Chapitre 3 -----
    "sentence21": {
        "FR": "Pour rembourser nos 200 000 €,",
        "EN": "To pay back our £200,000,",
        "ES": "Para devolver nuestros 200 000 €,",
        "PT": "Para pagar os 200 000 €,",
    },
    "sentence22": {
        "FR": "il faut verser une somme $M$ chaque mois pendant 20 ans.",
        "EN": "we must make a payment $M$ every month for 20 years.",
        "ES": "hay que pagar una cuota $M$ cada mes durante 20 años.",
        "PT": "é preciso pagar uma prestação $M$ todo mês por 20 anos.",
    },
    "sentence23": {
        "FR": "Et cette somme vaut de moins en moins en valeur actuelle.",
        "EN": "And each payment loses value in present terms.",
        "ES": "Y cada pago vale menos en términos de valor presente.",
        "PT": "Cada pagamento vale menos em valor presente.",
    },
    "sentence24": {
        "FR": "L’équation à résoudre pour connaître la mensualité est :",
        "EN": "The equation to solve for the monthly payment is:",
        "ES": "La ecuación para calcular la cuota mensual es:",
        "PT": "A equação para calcular a prestação mensal é:",
    },
    "sentence25": {
        "FR": r"$200 000 \text{€}= \dfrac{M}{1+i} + \dfrac{M}{(1+i)^{2}} + \dfrac{M}{(1+i)^{3}} + \dots + \dfrac{M}{(1+i)^{240}}$.",
        "EN": r"$200{,}000 \text{£} = \dfrac{M}{1+i} + \dfrac{M}{(1+i)^{2}} + \dfrac{M}{(1+i)^{3}} + \dots + \dfrac{M}{(1+i)^{240}}$.",
        "ES": r"$200 000 \text{€} = \dfrac{M}{1+i} + \dfrac{M}{(1+i)^{2}} + \dfrac{M}{(1+i)^{3}} + \dots + \dfrac{M}{(1+i)^{240}}$.",
        "PT": r"$200 000  \text{€}= \dfrac{M}{1+i} + \dfrac{M}{(1+i)^{2}} + \dfrac{M}{(1+i)^{3}} + \dots + \dfrac{M}{(1+i)^{240}}$.",
    },

    "sentence31": {
        "FR": r"On peut réécrire : $200000 \text{€} = M \sum_{k=1}^{240} \dfrac{1}{(1+i)^{k}}$.",
        "EN": r"We can rewrite this as: $\text{£} 200{,}000 = M \sum_{k=1}^{240} \dfrac{1}{(1+i)^{k}}$.",
        "ES": r"Se puede reescribir así: $200 000 \text{€}= M \sum_{k=1}^{240} \dfrac{1}{(1+i)^{k}}$.",
        "PT": r"Podemos reescrever assim: $200 000 \text{€}= M \sum_{k=1}^{240} \dfrac{1}{(1+i)^{k}}$.",
    },
    "sentence32": {
        "FR": r"On reconnaît une série géométrique de la forme $\sum_{k=1}^{N} q^{k}$.",
        "EN": r"This is a geometric series of the form $\sum_{k=1}^{N} q^{k}$.",
        "ES": r"Reconocemos una serie geométrica de la forma $\sum_{k=1}^{N} q^{k}$.",
        "PT": r"Reconhecemos uma série geométrica da forma $\sum_{k=1}^{N} q^{k}$.",
    },
    "sentence33": {
        "FR": "On peut alors utiliser la formule bien connue :",
        "EN": "We can then use the well-known formula:",
        "ES": "Entonces podemos usar la fórmula conocida:",
        "PT": "Podemos então usar a fórmula conhecida:",
    },
    "sentence34": {
        "FR": r"$\sum_{k=1}^{N} q^{k} = \dfrac{q(1 - q^{N})}{1-q}$.",
        "EN": r"$\sum_{k=1}^{N} q^{k} = \dfrac{q(1 - q^{N})}{1-q}$.",
        "ES": r"$\sum_{k=1}^{N} q^{k} = \dfrac{q(1 - q^{N})}{1-q}$.",
        "PT": r"$\sum_{k=1}^{N} q^{k} = \dfrac{q(1 - q^{N})}{1-q}$.",
    },
  #  "sentence36": {
  #      "FR": r"Ainsi $200000 \text{€} = M \times \dfrac{1 - (1+i)^{-240}}{i}$.",
  #      "EN": r"So $ \text{£} 200{,}000 = M \times \dfrac{1 - (1+i)^{-240}}{i}$.",
  #      "ES": r"Así $200 000 \text{€}= M \times \dfrac{1 - (1+i)^{-240}}{i}$.",
  #      "PT": r"Assim $200 000 \text{€}= M \times \dfrac{1 - (1+i)^{-240}}{i}$.",
  #  },
    
    "sentence35": {
        "FR": r"""$
            \begin{array}{rcl}
                200000 \text{€} &=& M \times \dfrac{1 - (1+i)^{-240}}{i}\\
                        &=& M \times \dfrac{1 - (1+0.25 \%)^{-240}}{0.25 \%}.
            \end{array}$
        """,
        "EN": r"""$
            \begin{array}{rcl}
                \text{£}200000  &=& M \times \dfrac{1 - (1+i)^{-240}}{i}\\
                        &=& M \times \dfrac{1 - (1+0.25 \%)^{-240}}{0.25 \%}.
            \end{array}$
        """,
        "ES": r"""$
            \begin{array}{rcl}
                200000 \text{€} &=& M \times \dfrac{1 - (1+i)^{-240}}{i}\\
                        &=& M \times \dfrac{1 - (1+0.25 \%)^{-240}}{0.25 \%}.
            \end{array}$
        """,
        "PT": r"""$
            \begin{array}{rcl}
                200000 \text{€} &=& M \times \dfrac{1 - (1+i)^{-240}}{i}\\
                        &=& M \times \dfrac{1 - (1+0.25 \%)^{-240}}{0.25 \%}.
            \end{array}$
        """,
    },




    # ----- Chapitre 4 -----
    "sentence41": {
        "FR": "Cette formule permet de calculer la mensualité :",
        "EN": "This formula gives the monthly payment:",
        "ES": "Esta fórmula permite calcular la cuota mensual:",
        "PT": "Esta fórmula permite calcular a prestação mensal:",
    },
    "sentence42": {
        "FR": r"$M = 200000 \text{€} \times \dfrac{0.25 \%}{1 - (1+0.25 \%)^{-240}} \;\approx\; 1 109 \,\text{€}$.",
        "EN": r"$M = \text{£} 200{,}000  \times \dfrac{0.25 \%}{1 - (1+0.25 \%)^{-240}} \;\approx\; \text{£}1{,}109$.",
        "ES": r"$M = 200 000 \text{€} \times \dfrac{0.25 \%}{1 - (1+0.25 \%)^{-240}} \;\approx\; 1 109 \,\text{€}$.",
        "PT": r"$M = 200 000 \text{€} \times \dfrac{0.25 \%}{1 - (1+0.25 \%)^{-240}} \;\approx\; 1 109 \,\text{€}$.",
    },
    "sentence43": {
        "FR": r"Le coût total du prêt est alors $240 \times M \approx 266\,207 \,\text{€}$.",
        "EN": r"The total cost of the loan is then $240 \times M \approx \text{£}266{,}207$.",
        "ES": r"El costo total del préstamo es entonces $240M \approx 266\,207 \,\text{€}$.",
        "PT": r"O custo total do empréstimo é então $240 \times M \approx 266\,207 \,\text{€}$.",
    },
    "sentence44": {
        "FR": "empty.",
        "EN": "empty.",
        "ES": "empty.",
        "PT": "empty.",
    },
    "sentence45": {
        "FR": r"Pour un taux d'intérêt annuel de $2\%$, $M = 1 012 \text{€}$,",
        "EN": r"For an annual interest rate of $2\%$, $M = \text{£}1{,}012$,",
        "ES": r"Para una tasa de interés anual del $2\%$, $M = 1 012 \,\text{€}$,",
        "PT": r"Para uma taxa de juros anual de $2\%$, $M = 1 012 \,\text{€}$,",
    },
    "sentence46": {
        "FR": r"et pour $4\%$, $M = 1 212 \text{€}$.",
        "EN": r"and for $4\%$, $M = \text{£}1{,}212$.",
        "ES": r"y para un $4\%$, $M = 1 212 \,\text{€}$.",
        "PT": r"e para $4\%$, $M = 1 212 \,\text{€}$.",
    },


    "cta_sub": {
        "FR": "Explorez plus de maths et d’astrophysique — abonnez-vous !",
        "EN": "Discover more math & astrophysics — subscribe!",
        "ES": "Descubre más matemáticas y astrofísica — ¡suscríbete!",
        "PT": "Descubra mais matemática e astrofísica — inscreva-se!",
    },
}

def t(key: str):
    """Return the object for the current language (str / ('math', ...) / dict)."""
    try:
        return TEXT[key][LANG]
    except KeyError:
        return f"[{key}:{LANG} MISSING]"
