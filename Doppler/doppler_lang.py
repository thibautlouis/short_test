# cow_lang.py
import os

LANG = os.getenv("SHORT_LANG", "FR")  # FR par défaut

TEXT = {
    # ----- Titre -----
    "title": {
        "FR": "Mesurer l'expansion de l'Univers",
        "EN": "Measuring the Universe’s Expansion",
        "ES": "Cómo medir la expansión del Universo",
        "PT": "Medindo a expansão do Universo",
    },
    # ----- Intro -----
    "sentence01": {
        "FR": "Imaginons la scène suivante.",
        "EN": "Imagine the following situation.",
        "ES": "Imagina la siguiente situación.",
        "PT": "Imagine a seguinte situação.",
    },
    "sentence02": {
        "FR": "Une ambulance immobile émet des ondes sonores.",
        "EN": "A parked ambulance is emitting sound waves.",
        "ES": "Una ambulancia detenida emite ondas sonoras.",
        "PT": "Uma ambulância parada emite ondas sonoras.",
    },
    "sentence03": {
        "FR": "Un passant sur le bord de la route mesure leur fréquence.",
        "EN": "Someone standing by the road measures their frequency.",
        "ES": "Un peatón al borde de la carretera mide su frecuencia.",
        "PT": "Um pedestre à beira da estrada mede a frequência delas.",
    },
    "sentence11": {
        "FR": "Mettons maintenant l'ambulance en mouvement.",
        "EN": "Now let’s get the ambulance moving.",
        "ES": "Ahora hagamos que la ambulancia se ponga en marcha.",
        "PT": "Agora vamos colocar a ambulância em movimento.",
    },
    "sentence12": {
        "FR": "Quand elle s'approche, la fréquence apparente de",
        "EN": "As it comes closer, the pitch of",
        "ES": "Cuando se acerca, el tono de",
        "PT": "Quando ela se aproxima, o tom da",
    },
    "sentence13": {
        "FR": "la sirène augmente, quand elle s'éloigne elle diminue.",
        "EN": "the siren sounds higher; as it moves away, lower.",
        "ES": "la sirena suena más agudo; cuando se aleja, más grave.",
        "PT": "sirene soa mais agudo; quando se afasta, mais grave.",
    },
    "sentence21": {
        "FR": "Cet effet, l'effet Doppler, a une conséquence physique",
        "EN": "This is the Doppler effect, it has a powerful consequence:",
        "ES": "Este es el efecto Doppler; tiene una consecuencia:",
        "PT": "Esse é o efeito Doppler; ele tem uma consequência:"
    },
    "sentence22": {
        "FR": "intéressante : il permet de mesurer la vitesse d'un objet",
        "EN": "it lets us measure how fast an object is moving",
        "ES": "nos permite medir qué tan rápido se mueve un objeto",
        "PT": "ele nos permite medir a velocidade de um objeto",
    },
    "sentence23": {
        "FR": "à partir de la fréquence apparente des ondes qu'il émet.",
        "EN": "just by looking at the waves it emits.",
        "ES": "solo observando las ondas que emite.",
        "PT": "apenas observando as ondas que ele emite.",
    },
    "sentence31": {
        "FR": "Cet effet est essentiel pour mesurer l’expansion",
        "EN": "And this effect is essential to measure the expansion",
        "ES": "Y este efecto es esencial para medir la expansión",
        "PT": "E esse efeito é essencial para medir a expansão",
    },
    "sentence32": {
        "FR": "de l’Univers. Quand une galaxie s’éloigne de nous, ",
        "EN": "of the Universe. When a galaxy drifts away,",
        "ES": "del Universo. Cuando una galaxia se aleja,",
        "PT": "do Universo. Quando uma galáxia se afasta,",
    },
    "sentence33": {
        "FR": "la fréquence de sa lumière diminue.",
        "EN": "the frequency of its light shifts lower.",
        "ES": "la frecuencia de su luz se hace menor.",
        "PT": "a frequência da sua luz diminui.",
    },
    "sentence34": {
        "FR": "On appelle ce phénomène le décalage vers le rouge.",
        "EN": "This phenomenon is called redshift.",
        "ES": "A este fenómeno lo llamamos corrimiento al rojo.",
        "PT": "Esse fenômeno é chamado de desvio para o vermelho.",
    },
    "sentence35": {
        "FR": "Il nous permet de mesurer la vitesse de galaxies",
        "EN": "It allows us to measure the speed of galaxies",
        "ES": "Nos permite medir la velocidad de galaxias",
        "PT": "Ele nos permite medir a velocidade de galáxias",
    },
    "sentence36": {
        "FR": "situées à des milliards d’années-lumière.",
        "EN": "billions of light-years away.",
        "ES": "a miles de millones de años luz de distancia.",
        "PT": "a bilhões de anos-luz de distância.",
    },
    "sentence41": {
        "FR": "Aujourd’hui, la mesure de ce décalage est au cœur",
        "EN": "Today, measuring this redshift is at the heart",
        "ES": "Hoy, medir este corrimiento está en el centro",
        "PT": "Hoje, medir esse desvio está no centro",
    },
    "sentence42": {
        "FR": "de débats qui agitent les cosmologistes.",
        "EN": "of debates that stir cosmologists.",
        "ES": "de debates que dividen a los cosmólogos.",
        "PT": "de debates que agitam os cosmólogos.",
    },
    "sentence43": {
        "FR": "L’expansion de l’Univers apparaît accélérée ce qui",
        "EN": "The Universe seems to be expanding faster and faster, ",
        "ES": "El Universo parece expandirse cada vez más rápido, ",
        "PT": "O Universo parece estar se expandindo cada vez mais rápido, ",
    },
    "sentence44": {
        "FR": "suggère qu’une partie de son énergie est",
        "EN": "which suggests that part of its energy exists",
        "ES": "lo que sugiere que parte de su energía está",
        "PT": "o que sugere que parte da sua energia está",
    },
    "sentence45": {
        "FR": "sous une forme mystérieuse qu’on appelle l’énergie sombre.",
        "EN": "in a mysterious form we call dark energy.",
        "ES": "en una forma misteriosa que llamamos energía oscura.",
        "PT": "em uma forma misteriosa que chamamos de energia escura.",
    },
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
