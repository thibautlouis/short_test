# time_dilatation_lang.py
import os

LANG = os.getenv("SHORT_LANG", "FR")  # FR par défaut

TEXT = {
    # ----- Titre -----
    "title": {
        "FR": "Dilatation du temps",
        "EN": "Time Dilation",
        "ES": "Dilatación del tiempo",
        "PT": "Dilatação do tempo",
    },

    # ----- Chapitre 1 : expérience de pensée -----
    "sentence01": {
        "FR": "Albert Einstein a imaginé l’expérience de pensée suivante.",
        "EN": "Einstein imagined the following thought experiment.",
        "ES": "Albert Einstein imaginó el siguiente experimento mental.",
        "PT": "Albert Einstein imaginou o seguinte experimento mental.",
    },
    "sentence02": {
        "FR": "Un photon rebondit entre deux miroirs parallèles,",
        "EN": "A photon bounces back and forth between two mirrors,",
        "ES": "Un fotón rebota entre dos espejos paralelos,",
        "PT": "Um fóton vai e volta entre dois espelhos paralelos,",
    },
    "sentence03": {
        "FR": r"séparés par une distance $L$.",
        "EN": r"separated by a distance $L$.",
        "ES": r"separados por una distancia $L$.",
        "PT": r"separados por uma distância $L$.",
    },
    "sentence04": {
        "FR": r"Le temps d’un aller-retour vaut $\Delta t = 2L/c$",
        "EN": r"The round trip takes $\Delta t = 2L/c$",
        "ES": r"El recorrido de ida y vuelta dura $\Delta t = 2L/c$",
        "PT": r"A viagem de ida e volta leva $\Delta t = 2L/c$",
    },
    "sentence05": {
        "FR": r"où $c$ est la vitesse de la lumière.",
        "EN": r"where $c$ is the speed of light.",
        "ES": r"donde $c$ es la velocidad de la luz.",
        "PT": r"onde $c$ é a velocidade da luz.",
    },

    # ----- Chapitre 2 : la même expérience en mouvement -----
    "sentence11": {
        "FR": "Plaçons maintenant ces miroirs à bord d’un train,",
        "EN": "Now let’s put these mirrors inside a moving train,",
        "ES": "Ahora pongamos estos espejos dentro de un tren,",
        "PT": "Agora coloquemos esses espelhos dentro de um trem,",
    },
    "sentence12": {
        "FR": r"qui roule à la vitesse $v$.",
        "EN": r"traveling at speed $v$.",
        "ES": r"que avanza a velocidad $v$.",
        "PT": r"que se move a uma velocidade $v$.",
    },
    "sentence13": {
        "FR": r"Pour un passager, rien ne change : $\Delta t_{\rm train} = 2L/c$.",
        "EN": r"For a passenger, nothing changes: $\Delta t_{\rm train} = 2L/c$.",
        "ES": r"Para un pasajero, nada cambia: $\Delta t_{\rm tren} = 2L/c$.",
        "PT": r"Para o passageiro, nada muda: $\Delta t_{\rm trem} = 2L/c$.",
    },
    "sentence14": {
        "FR": "Mais, pour un observateur assis sur le quai,",
        "EN": "But for an observer sitting on the platform,",
        "ES": "Pero, para un observador sentado en el andén,",
        "PT": "Mas, para um observador sentado na plataforma,",
    },
    "sentence15": {
        "FR": "la lumière suit un trajet oblique.",
        "EN": "the light follows an oblique path.",
        "ES": "la luz sigue un trayecto oblicuo.",
        "PT": "a luz segue um trajeto oblíquo.",
    },

    # ----- Chapitre 3 : calcul sur le quai -----
    "sentence21": {
        "FR": r"On peut calculer le temps de trajet de la lumière $\Delta t_{\rm quai}$",
        "EN": r"We can calculate the light’s travel time $\Delta t_{\rm platform}$",
        "ES": r"Podemos calcular el tiempo del recorrido de la luz $\Delta t_{\rm anden}$",
        "PT": r"Podemos calcular o tempo do percurso da luz $\Delta t_{\rm plataforma}$",
    },
    "sentence22": {
        "FR": "pour l’observateur immobile sur le quai.",
        "EN": "for the stationary observer on the platform.",
        "ES": "para el observador quieto en el andén.",
        "PT": "para o observador parado na plataforma.",
    },
    "sentence23": {
        "FR": "Avec le théorème de Pythagore, on trouve :",
        "EN": "Using Pythagoras’ theorem, we get:",
        "ES": "Con el teorema de Pitágoras, obtenemos:",
        "PT": "Com o teorema de Pitágoras, obtemos:",
    },
    "sentence24": {
        "FR": r"$\left(\tfrac{c\,\Delta t_{\rm quai}}{2}\right)^2 = L^2 + \left(\tfrac{v\,\Delta t_{\rm quai}}{2}\right)^2$",
        "EN": r"$\left(\tfrac{c\,\Delta t_{\rm platform}}{2}\right)^2 = L^2 + \left(\tfrac{v\,\Delta t_{\rm platform}}{2}\right)^2$",
        "ES": r"$\left(\tfrac{c\,\Delta t_{\rm anden}}{2}\right)^2 = L^2 + \left(\tfrac{v\,\Delta t_{\rm anden}}{2}\right)^2$",
        "PT": r"$\left(\tfrac{c\,\Delta t_{\rm plataforma}}{2}\right)^2 = L^2 + \left(\tfrac{v\,\Delta t_{\rm plataforma}}{2}\right)^2$",
    },
    "sentence25": {
        "FR": r"En isolant $\Delta t_{\rm quai}$, on obtient :",
        "EN": r"Isolating $\Delta t_{\rm platform}$ gives:",
        "ES": r"Si aislamos $\Delta t_{\rm anden}$, obtenemos:",
        "PT": r"Ao isolar $\Delta t_{\rm plataforma}$, obtemos:",
    },
    "sentence26": {
        "FR": r"$\Delta t_{\rm quai} = \dfrac{2L}{c}\,\dfrac{1}{\sqrt{1 - v^2/c^2}} = \dfrac{\Delta t_{\rm train} }{\sqrt{1 - v^2/c^2}}$",
        "EN": r"$\Delta t_{\rm platform} = \dfrac{2L}{c}\,\dfrac{1}{\sqrt{1 - v^2/c^2}} = \dfrac{\Delta t_{\rm train} }{\sqrt{1 - v^2/c^2}}$",
        "ES": r"$\Delta t_{\rm anden} = \dfrac{2L}{c}\,\dfrac{1}{\sqrt{1 - v^2/c^2}} = \dfrac{\Delta t_{\rm tren} }{\sqrt{1 - v^2/c^2}}$",
        "PT": r"$\Delta t_{\rm plataforma} = \dfrac{2L}{c}\,\dfrac{1}{\sqrt{1 - v^2/c^2}} = \dfrac{\Delta t_{\rm trem} }{\sqrt{1 - v^2/c^2}}$",
    },
    "sentence27": {
        "FR": r"$\Delta t_{\rm quai} \neq \Delta t_{\rm train}$ : le temps n’est pas absolu !",
        "EN": r"$\Delta t_{\rm platform} \neq \Delta t_{\rm train}$: time is not absolute!",
        "ES": r"$\Delta t_{\rm anden} \neq \Delta t_{\rm tren}$: ¡el tiempo no es absoluto!",
        "PT": r"$\Delta t_{\rm plataforma} \neq \Delta t_{\rm trem}$: o tempo não é absoluto!",
    },

    # ----- Chapitre 4 : exemple numérique -----
    "sentence31": {
        "FR": r"Supposons que le passager mesure $\Delta t_{\rm train} = 1\,\mathrm{s}$,",
        "EN": r"Suppose the passenger measures $\Delta t_{\rm train} = 1\,\mathrm{s}$,",
        "ES": r"Supongamos que el pasajero mide $\Delta t_{\rm tren} = 1\,\mathrm{s}$,",
        "PT": r"Suponha que o passageiro meça $\Delta t_{\rm trem} = 1\,\mathrm{s}$,",
    },
    "sentence32": {
        "FR": r"si le train va à $80\%$ de la vitesse de la lumière.",
        "EN": r"if the train goes at $80\%$ of the speed of light.",
        "ES": r"si el tren va al $80\%$ de la velocidad de la luz.",
        "PT": r"se o trem vai a $80\%$ da velocidade da luz.",
    },
    "sentence33": {
        "FR": r"$\Delta t_{\rm quai} \approx 1{,}67\,\mathrm{s}$ : le passager vieillit moins vite",
        "EN": r"$\Delta t_{\rm platform} \approx 1.67\,\mathrm{s}$: the passenger ages more slowly",
        "ES": r"$\Delta t_{\rm anden} \approx 1{,}67\,\mathrm{s}$: el pasajero envejece más despacio",
        "PT": r"$\Delta t_{\rm plataforma} \approx 1{,}67\,\mathrm{s}$: o passageiro envelhece mais lento",
    },
    "sentence34": {
        "FR": "que la personne restée sur le quai !",
        "EN": "than the person standing on the platform!",
        "ES": "que la persona que se quedó en el andén.",
        "PT": "do que a pessoa que ficou na plataforma!",
    },
    "sentence35": {
        "FR": "Le temps est relatif et dépend donc de l’observateur.",
        "EN": "Time is relative, and it depends on the observer.",
        "ES": "El tiempo es relativo y depende del observador.",
        "PT": "O tempo é relativo e depende do observador.",
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
