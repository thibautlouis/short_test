import os

LANG = os.getenv("SHORT_LANG", "FR")  # FR par défaut

TEXT = {
    # ----- Titre -----
    "title": {
        "FR": "Le paradoxe des anniversaires",
        "EN": "The Birthday Paradox",
        "ES": "La paradoja de los cumpleaños",
        "PT": "O paradoxo dos aniversários",
    },
    "sentence01": {
        "FR": "Imaginons une salle remplie de coffres au trésor.",
        "EN": "Imagine a room filled with treasure chests.",
        "ES": "Imaginemos una sala llena de cofres del tesoro.",
        "PT": "Imaginemos uma sala cheia de baús do tesouro.",
    },
    "sentence02": {
        "FR": "Chaque coffre déborde de richesses.",
        "EN": "Each chest overflows with riches.",
        "ES": "Cada cofre rebosa de riquezas.",
        "PT": "Cada baú transborda de riquezas.",
    },
    "sentence03": {
        "FR": "Une équipe de cinq joueurs participe au jeu suivant.",
        "EN": "A team of five players plays the following game.",
        "ES": "Un equipo de cinco jugadores juega al siguiente juego.",
        "PT": "Uma equipe de cinco jogadores participa do seguinte jogo.",
    },
    "sentence04": {
        "FR": "Chaque joueur entre l’un après l’autre et doit choisir",
        "EN": "Each player enters one after another and must choose",
        "ES": "Cada jugador entra uno tras otro y debe elegir",
        "PT": "Cada jogador entra um após o outro e deve escolher",
    },
    "sentence05": {
        "FR": "un coffre : si le coffre est plein, il rafle le butin,",
        "EN": "a chest: if it’s full, they grab the loot,",
        "ES": "un cofre: si está lleno, se lleva el botín,",
        "PT": "um baú: se estiver cheio, leva o tesouro,",
    },
    "sentence06": {
        "FR": "si le coffre a déjà été vidé, la partie s’arrête.",
        "EN": "if the chest was already emptied, the game ends.",
        "ES": "si el cofre ya fue vaciado, la partida termina.",
        "PT": "se o baú já tiver sido esvaziado, o jogo acaba.",
    },
    "sentence11": {
        "FR": "Ici, le joueur 4 a choisi le même coffre que le joueur 2.",
        "EN": "Here, player 4 picked the same chest as player 2.",
        "ES": "Aquí, el jugador 4 eligió el mismo cofre que el jugador 2.",
        "PT": "Aqui, o jogador 4 escolheu o mesmo baú que o jogador 2.",
    },
    "sentence12": {
        "FR": "Ce qui provoque l’arrêt du jeu.",
        "EN": "That’s what ends the game.",
        "ES": "Y eso provoca el fin del juego.",
        "PT": "E isso põe fim ao jogo.",
    },
    "sentence13": {
        "FR": "On peut alors se poser la question suivante :",
        "EN": "So we can ask the following question:",
        "ES": "Entonces podemos hacernos la siguiente pregunta:",
        "PT": "Podemos então fazer a seguinte pergunta:",
    },
    "sentence14": {
        "FR": "quelle est la probabilité que tous les joueurs",
        "EN": "what is the probability that all players",
        "ES": "¿cuál es la probabilidad de que todos los jugadores",
        "PT": "qual é a probabilidade de que todos os jogadores",
    },
    "sentence15": {
        "FR": "ouvrent des coffres différents ?",
        "EN": "open different chests?",
        "ES": "abran cofres distintos?",
        "PT": "abram baús diferentes?",
    },
    "sentence21": {
        "FR": "Pour le $2^{e}$ joueur : 5 coffres sont libres sur 6.",
        "EN": "For the 2nd player: 5 out of 6 chests are free.",
        "ES": "Para el 2º jugador: 5 cofres libres de 6.",
        "PT": "Para o 2º jogador: 5 de 6 baús estão livres.",
    },
    "sentence22": {
        "FR": "Pour le $3^{e}$ : seulement 4 sur 6.",
        "EN": "For the 3rd: only 4 out of 6.",
        "ES": "Para el 3º: solo 4 de 6.",
        "PT": "Para o 3º: apenas 4 de 6.",
    },
    "sentence23": {
        "FR": r"Pour le $4^{e}$ : 3 sur 6, et 2 sur 6 pour le $5^{e}$.",
        "EN": r"For the 4th: 3 out of 6, and 2 out of 6 for the 5th.",
        "ES": r"Para el 4º: 3 de 6, y 2 de 6 para el 5º.",
        "PT": r"Para o 4º: 3 de 6, e 2 de 6 para o 5º.",
    },
    "sentence24": {
        "FR": r"La probabilité du gain maximal est donc :",
        "EN": r"The probability of the maximum gain is therefore:",
        "ES": r"La probabilidad del máximo beneficio es entonces:",
        "PT": r"A probabilidade do ganho máximo é então:",
    },
    "sentence25": {
        "FR": r"$P = \tfrac{5}{6}\times\tfrac{4}{6}\times\tfrac{3}{6}\times\tfrac{2}{6}\approx 9\%$.",
        "EN": r"$P = \tfrac{5}{6}\times\tfrac{4}{6}\times\tfrac{3}{6}\times\tfrac{2}{6}\approx 9\%$.",
        "ES": r"$P = \tfrac{5}{6}\times\tfrac{4}{6}\times\tfrac{3}{6}\times\tfrac{2}{6}\approx 9\%$.",
        "PT": r"$P = \tfrac{5}{6}\times\tfrac{4}{6}\times\tfrac{3}{6}\times\tfrac{2}{6}\approx 9\%$.",
    },
    "sentence26": {
        "FR": "Réciproquement, la probabilité qu’il y ait au moins",
        "EN": "Conversely, the probability that there is at least",
        "ES": "En cambio, la probabilidad de que haya al menos",
        "PT": "Por outro lado, a probabilidade de que haja pelo menos",
    },
    "sentence27": {
        "FR": r"un doublon est $P_{\rm doublon} = 1 - P \approx 91\%$.",
        "EN": r"one overlap is $P_{\rm duplicate} = 1 - P \approx 91\%$.",
        "ES": r"una coincidencia es $P_{\rm coincidencia} = 1 - P \approx 91\%$.",
        "PT": r"uma repetição é $P_{\rm repeticao} = 1 - P \approx 91\%$.",
    },
    "sentence31": {
        "FR": "Ce petit calcul se transpose dans un paradoxe",
        "EN": "This simple calculation connects to a famous paradox:",
        "ES": "Este cálculo sencillo se traduce en una paradoja conocida:",
        "PT": "Esse cálculo simples leva a um paradoxo famoso:",
    },
    "sentence32": {
        "FR": "bien connu : le paradoxe des anniversaires.",
        "EN": "the birthday paradox.",
        "ES": "la paradoja de los cumpleaños.",
        "PT": "o paradoxo dos aniversários.",
    },
    "sentence33": {
        "FR": "Dans une classe de 24 élèves, quelle est la probabilité",
        "EN": "In a class of 24 students, what is the probability",
        "ES": "En una clase de 24 alumnos, ¿cuál es la probabilidad",
        "PT": "Numa turma de 24 alunos, qual é a probabilidade",
    },
    "sentence34": {
        "FR": "que deux enfants aient leur anniversaire le même jour ?",
        "EN": "that two of them share the same birthday?",
        "ES": "de que dos compartan el mismo cumpleaños?",
        "PT": "de que dois façam aniversário no mesmo dia?",
    },
    "sentence35": {
        "FR": r"$P_{\rm doublon} = 1 - \tfrac{364}{365}\times\tfrac{363}{365}\times \cdots \times \tfrac{(365 - 24 + 1)}{365}$",
        "EN": r"$P_{\rm duplicate} = 1 - \tfrac{364}{365}\times\tfrac{363}{365}\times \cdots \times \tfrac{(365 - 24 + 1)}{365}$",
        "ES": r"$P_{\rm coincidencia} = 1 - \tfrac{364}{365}\times\tfrac{363}{365}\times \cdots \times \tfrac{(365 - 24 + 1)}{365}$",
        "PT": r"$P_{\rm repeticao} = 1 - \tfrac{364}{365}\times\tfrac{363}{365}\times \cdots \times \tfrac{(365 - 24 + 1)}{365}$",
    },
    "sentence36": {
        "FR": r"Le résultat est surprenant : $P_{\rm doublon} \approx 50\%$,",
        "EN": r"The result is surprising: $P_{\rm duplicate} \approx 50\%$,",
        "ES": r"El resultado es sorprendente: $P_{\rm coincidencia} \approx 50\%$,",
        "PT": r"O resultado é surpreendente: $P_{\rm repeticao} \approx 50\%$,",
    },
    "sentence37": {
        "FR": r"Une chance sur deux de partager un anniversaire !",
        "EN": r"One in two chance of sharing a birthday!",
        "ES": r"Una de dos de compartir cumpleaños!",
        "PT": r"Uma em duas de compartilhar aniversário!",
    },
    "sentence38": {
        "FR": r"Les coïncidences sont bien moins rares qu’on le pense.",
        "EN": r"Coincidences are far less rare than we think.",
        "ES": r"Las coincidencias son menos raras de lo que creemos.",
        "PT": r"As coincidências são muito menos raras do que pensamos.",
    },

    # ----- Call-to-action -----
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
