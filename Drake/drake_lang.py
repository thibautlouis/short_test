import os

LANG = os.getenv("SHORT_LANG", "FR")  # FR par défaut

TEXT = {
    # ----- Titre -----
    "title": {
        "FR": "L’équation des civilisations",
        "EN": "The Civilizations Equation",
        "ES": "La ecuación de las civilizaciones",
        "PT": "A equação das civilizações",
    },
    "short_title": {
        "FR": "L’équation des civilisations",
        "EN": "The Civilizations Equation",
        "ES": "La ecuación de las civilizaciones",
        "PT": "A equação das civilizações",
    },
    # ----- Labels courts pour l’intro “graphique” -----
    "lab_N": {
        "FR": "Nombre de civilisations détectables dans la Voie lactée",
        "EN": "Number of detectable civilizations in the Milky Way",
        "ES": "Número de civilizaciones detectables en la Vía Láctea",
        "PT": "Número de civilizações detectáveis na Via Láctea",
    },
    "lab_Rs": {
        "FR": "Taux de formation d'étoiles",
        "EN": "Star formation rate",
        "ES": "Tasa de formación estelar",
        "PT": "Taxa de formação estelar",
    },
    "lab_fp": {
        "FR": "Fraction d’étoiles avec planètes",
        "EN": "Fraction of stars with planets",
        "ES": "Fracción de estrellas con planetas",
        "PT": "Fração de estrelas com planetas",
    },
    "lab_ne": {
        "FR": "Nombre de planètes habitables par système",
        "EN": "number of habitable planets per system",
        "ES": "Número medio de planetas habitables por sistema",
        "PT": "Número médio de planetas habitáveis por sistema",
    },
    "lab_fl": {
        "FR": "Fraction des planètes où la vie apparaît",
        "EN": "Fraction where life appears",
        "ES": "Fracción donde aparece la vida",
        "PT": "Fração em que surge a vida",
    },
    "lab_fi": {
        "FR": "Fraction des cas où la vie évolue vers l’intelligence",
        "EN": "Fraction where life evolves toward intelligence",
        "ES": "Fracción donde la vida evoluciona hacia la inteligencia",
        "PT": "Fração em que a vida evolui para a inteligência",
    },
    "lab_fc": {
        "FR": "Fraction des civilisations qui développent des technologies de communication",
        "EN": "Fraction that develop communication technology",
        "ES": "Fracción que desarrolla tecnologías de comunicación",
        "PT": "Fração que desenvolve tecnologias de comunicação",
    },
    "lab_L": {
        "FR": "Durée moyenne de survie des civilisations",
        "EN": "Average lifetime of civilizations",
        "ES": "Vida media de las civilizaciones",
        "PT": "Tempo médio de vida das civilizações",
    },

    # ----- Chapitre 1 : Contexte historique bref -----
    "sentence01": {
        "FR": "En 1961, Frank Drake propose une formule pour estimer",
        "EN": "In 1961, Frank Drake proposed a formula to estimate",
        "ES": "En 1961, Frank Drake propuso una fórmula para estimar",
        "PT": "Em 1961, Frank Drake propôs uma fórmula para estimar",
    },
    "sentence02": {
        "FR": "le nombre de civilisations de notre galaxie avec",
        "EN": "the number of civilizations in our galaxy with which",
        "ES": "el número de civilizaciones de nuestra galaxia con las",
        "PT": "o número de civilizações na nossa galáxia com as",
    },
    "sentence03": {
        "FR": "lesquelles nous pourrions entrer en contact.",
        "EN": "we could make contact.",
        "ES": "que podríamos establecer contacto.",
        "PT": "quais poderíamos estabelecer contato.",
    },
    "sentence04": {
        "FR": "Chaque terme décrit une étape : étoiles, planètes,",
        "EN": "Each term describes a step: stars, planets,",
        "ES": "Cada término describe una etapa: estrellas, planetas,",
        "PT": "Cada termo descreve uma etapa: estrelas, planetas,",
    },
    "sentence05": {
        "FR": "apparition de la vie, intelligence, communication, survie.",
        "EN": "appearance of life, intelligence, communication, survival.",
        "ES": "vida, inteligencia, comunicación, supervivencia.",
        "PT": "vida, inteligência, comunicação, sobrevivência.",
    },
    "sentence06": {
        "FR": "Bien qu’elle soit très incertaine, l’équation offre",
        "EN": "Although it is very uncertain, the equation offers",
        "ES": "Aunque es muy incierta, la ecuación ofrece",
        "PT": "Embora seja muito incerta, a equação oferece",
    },
    "sentence07": {
        "FR": "un cadre scientifique à cette question essentielle.",
        "EN": "a scientific framework for this essential question.",
        "ES": "un marco científico para esta cuestión esencial.",
        "PT": "um enquadramento científico para esta questão essencial.",
    },
    # ----- Chapitre 2 : Mesure -----
    "sentence11": {
        "FR": "Depuis, nos observations ont beaucoup progressé.",
        "EN": "Since then, our observations have advanced greatly.",
        "ES": "Desde entonces, hemos progresado mucho.",
        "PT": "Desde então, nossas observações avançaram muito.",
    },
    "sentence12": {
        "FR": "Le satellite Kepler, lancé en 2009, a détecté",
        "EN": "The Kepler satellite, launched in 2009, detected",
        "ES": "El satélite Kepler, lanzado en 2009, detectó",
        "PT": "O satélite Kepler, lançado em 2009, detectou",
    },
    "sentence13": {
        "FR": "plus de 2 600 exoplanètes, révélant que la plupart",
        "EN": "over 2,600 exoplanets, revealing that most",
        "ES": "más de 2.600 exoplanetas, revelando que la mayoría",
        "PT": "mais de 2.600 exoplanetas, revelando que a maioria",
    },
    "sentence14": {
        "FR": "des étoiles possèdent des planètes.",
        "EN": "stars host planets.",
        "ES": "de las estrellas tienen planetas.",
        "PT": "das estrelas tem planetas.",
    },
    "sentence15": {
        "FR": "empty.",
        "EN": "empty.",
        "ES": "empty.",
        "PT": "empty.",
    },
    "sentence16": {
        "FR": "Le télescope James-Webb observe désormais",
        "EN": "The James Webb telescope now observes",
        "ES": "El telescopio James Webb observa ahora",
        "PT": "O telescópio James Webb agora observa",
    },
    "sentence17": {
        "FR": "certaines de ces planètes en détail et analyse leur",
        "EN": "some of these planets in detail and analyzes their",
        "ES": "algunos de estos planetas en detalle y analiza sus",
        "PT": "alguns desses planetas em detalhe e analisa suas",
    },
    "sentence18": {
        "FR": "atmosphère pour y chercher des traces de vie.",
        "EN": "atmospheres in search of signs of life.",
        "ES": "atmósferas en busca de señales de vida.",
        "PT": "atmosferas em busca de sinais de vida.",
    },

    # ----- Chapitre 3 : Terre -----
    "sentence20": {
        "FR": "Mais certains paramètres de l’équation restent inconnus.",
        "EN": "But some parameters of the equation remain unknown.",
        "ES": "Algunos parámetros siguen desconocidos.",
        "PT": "Alguns parâmetros seguem desconhecidos.",
    },
    "sentence21": {
        "FR": "Sur Terre, une seule espèce a développé son",
        "EN": "On Earth, only one species has developed its",
        "ES": "En la Tierra, solo una especie ha desarrollado su",
        "PT": "Na Terra, apenas uma espécie desenvolveu sua",
    },
    "sentence22": {
        "FR": "intelligence et ses moyens de communication.",
        "EN": "intelligence and its means of communication.",
        "ES": "inteligencia y sus medios de comunicación.",
        "PT": "inteligência e seus meios de comunicação.",
    },
    "sentence23": {
        "FR": "Un fait peut-être lié à des conditions géologiques uniques.",
        "EN": "A fact perhaps tied to unique geological conditions.",
        "ES": "Un hecho quizá ligado a condiciones geológicas únicas.",
        "PT": "Um fato talvez ligado a condições geológicas únicas.",
    },
    "sentence24": {
        "FR": "empty.",
        "EN": "empty.",
        "ES": "empty.",
        "PT": "empty.",
    },
    "sentence25": {
        "FR": "L’équation de Drake guide le programme SETI :",
        "EN": "Drake’s equation guides the SETI program,",
        "ES": "La ecuación de Drake guía el programa SETI,",
        "PT": "A equação de Drake orienta o programa SETI,",
    },
    "sentence26": {
        "FR": "un réseau de télescopes qui scrute le ciel pour",
        "EN": "a network of telescopes that scans the sky to",
        "ES": "una red de telescopios que examina el cielo para",
        "PT": "uma rede de telescópios que vasculha o céu para",
    },
    "sentence27": {
        "FR": "capter de possibles signaux venus d’ailleurs.",
        "EN": "detect possible signals from elsewhere.",
        "ES": "captar posibles señales venidas de otros lugares.",
        "PT": "detectar possíveis sinais vindos de outros lugares.",
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
