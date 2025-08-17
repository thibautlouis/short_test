# expansion.py
import manim as mn
import numpy as np
import os

import manim_helper as mh
from expansion_lang import t, LANG
from expansion_title_card import show_expansion_title_card

# ---------- Config vidéo (9:16) ----------
mn.config.frame_width  = 9
mn.config.frame_height = 16
mn.config.pixel_width  = 1080
mn.config.pixel_height = 1920

BG  = mn.BLACK
OBS = "#F87171"   # halo observateur (rouge/orangé)
VEC_COLOR = "#E5E7EB"
GAL_COL = "#93C5FD"

# Z-index policy (≤5)
Z_GROUP   = 1
Z_GALAXY  = 2
Z_VECTOR  = 3
Z_TEXT    = 4
Z_HALO    = 5

# ---------- Assets ----------
# priorité aux fichiers francisés 'galaxie.png', fallback sur 'galaxy.png'
ASSET_PATHS = [
    "galaxy.png",
    "galaxy.png",
]
def find_galaxy_asset():
    for p in ASSET_PATHS:
        if os.path.exists(p):
            return p
    return None

def make_fallback_galaxy(size=0.12, color=GAL_COL):
    core = mn.Dot(radius=size*0.35, color=color).set_opacity(0.95)
    halo = mn.Circle(radius=size).set_stroke(color, width=1.0, opacity=0.35)
    g = mn.Group(halo, core)
    g.set_z_index(Z_GALAXY)
    return g

def make_galaxy_img(size=0.22):
    path = find_galaxy_asset()
    if path:
        img = mn.ImageMobject(path)
        target_h = 2*size
        if img.height > 1e-9:
            img.scale(target_h / img.height)
        img.set_z_index(Z_GALAXY)
        return img
    else:
        return make_fallback_galaxy(size=size)

# ---------- Utils ----------
def sample_points_disc(n, r_max, r_min=0.0, rng=None):
    rng = np.random.default_rng(None if rng is None else rng)
    pts = []
    while len(pts) < n:
        u = rng.random()
        r = (u ** 0.5) * r_max
        if r < r_min:
            continue
        th = rng.uniform(0, 2*np.pi)
        pts.append(np.array([r*np.cos(th), r*np.sin(th), 0.0]))
    return pts


class ShortsManual(mh.TextChaptersScene):
    """
    Flow :
      1) 2D standalone (reste affichée pendant Chapitre 1)
      2) Début Chapitre 2 : FadeOut 2D
      3) 1D modulaire (vecteurs, expansion, reset, changement d'observateur, etc.)
    """

    # ------------------------
    #        2D STANDALONE
    # ------------------------
    
    
    def setup_expansion_2d(self, n_galaxies=15, r_comoving=2.0, exclude_core=0.4,
                       sprite_size=0.22, halo_radius=0.4, halo_width=2.7,
                       rng_seed=42):
            """Place galaxies et halo au centre, sans lancer l'expansion."""
            comoving_pts = [np.array([0.0, 0.0, 0.0])]
            comoving_pts += sample_points_disc(n_galaxies, r_comoving, r_min=exclude_core, rng=rng_seed)

            galaxies = []
            for p in comoving_pts:
                g = make_galaxy_img(sprite_size)
                g.rotate(np.random.uniform(-0.3, 0.3))
                g.set_opacity(0.0)
                g._x0 = p.copy()
                g.set_z_index(Z_GALAXY)
                galaxies.append(g)
            self.add(*galaxies)
    
            s = mn.ValueTracker(1.0)
            center = self.anim_zone.get_center()
            units_to_px = (self.anim_zone.width) / (2 * r_comoving)

            def x_to_point_2d(x_vec3: np.ndarray) -> np.ndarray:
                return center + np.array([x_vec3[0]*units_to_px, x_vec3[1]*units_to_px, 0.0])

            def galaxy_updater_2d(mob: mn.Mobject):
                x_phys = mob._x0 * s.get_value()
                mob.move_to(x_to_point_2d(x_phys))

            for g in galaxies:
                g.add_updater(galaxy_updater_2d)

            obs_glow_2d = mn.Circle(radius=halo_radius).set_stroke(OBS, width=halo_width)
            obs_glow_2d.set_z_index(Z_HALO)
            obs_glow_2d.move_to(x_to_point_2d(np.array([0.0, 0.0, 0.0])))
            self.add(obs_glow_2d)

            grp = mn.Group(*galaxies, obs_glow_2d)
            grp.set_z_index(Z_GROUP)
            self._center_group = grp

            self._exp2d = {
                "galaxies": galaxies,
                "s": s,
                "x_to_point": x_to_point_2d,
                "group": grp,
                "halo": obs_glow_2d,
                "galaxy_updater_2d": galaxy_updater_2d,
            }

            # fade-in galaxies uniquement
            self.play(*[g.animate.set_opacity(1.0) for g in galaxies], run_time=0.6)


    def play_expansion_only(self, s_target=2.2, expand_rt=4.6):
        """Joue uniquement l’expansion après coup."""
        s = self._exp2d["s"]
        self.play(s.animate.set_value(s_target), run_time=expand_rt, rate_func=mn.rate_functions.ease_in_out_sine)
        self.wait(0.2)

    
    
    def play_expansion_2d_standalone(
        self,
        n_galaxies=15,
        r_comoving=2.0,
        exclude_core=0.4,
        sprite_size=0.22,
        s_target=2.2,
        fadein_rt=0.6,
        expand_rt=4.6,
        rng_seed=42,
        halo_radius=0.4,
        halo_width=2.7,
    ):
        # Points comobiles
        comoving_pts = [np.array([0.0, 0.0, 0.0])]
        comoving_pts += sample_points_disc(n_galaxies, r_comoving, r_min=exclude_core, rng=rng_seed)

        # Galaxies
        galaxies = []
        for p in comoving_pts:
            g = make_galaxy_img(sprite_size)
            g.rotate(np.random.uniform(-0.3, 0.3))
            g.set_opacity(0.0)
            g._x0 = p.copy()  # position comobile 2D
            g.set_z_index(Z_GALAXY)
            galaxies.append(g)
        self.add(*galaxies)

        # Trackers & mapping
        s = mn.ValueTracker(1.0)
        center = self.anim_zone.get_center()
        units_to_px = (self.anim_zone.width) / (2 * r_comoving)

        def x_to_point_2d(x_vec3: np.ndarray) -> np.ndarray:
            return center + np.array([x_vec3[0]*units_to_px, x_vec3[1]*units_to_px, 0.0])

        def galaxy_updater_2d(mob: mn.Mobject):
            x_phys = mob._x0 * s.get_value()
            mob.move_to(x_to_point_2d(x_phys))

        for g in galaxies:
            g.add_updater(galaxy_updater_2d)

        # Halo observateur au centre
        obs_glow_2d = mn.Circle(radius=halo_radius).set_stroke(OBS, width=halo_width)
        obs_glow_2d.set_z_index(Z_HALO)
        obs_glow_2d.move_to(x_to_point_2d(np.array([0.0, 0.0, 0.0])))
        self.add(obs_glow_2d)

        # Group pour clean
        grp = mn.Group(*galaxies, obs_glow_2d)
        grp.set_z_index(Z_GROUP)
        self._center_group = grp

        # Animations 2D
        self.play(*[g.animate.set_opacity(1.0) for g in galaxies], run_time=fadein_rt)
        self.play(s.animate.set_value(s_target), run_time=expand_rt, rate_func=mn.rate_functions.ease_in_out_sine)
        self.wait(0.2)

        # Sauvegarde de l'état 2D si besoin ultérieur
        self._exp2d = {
            "galaxies": galaxies,
            "s": s,
            "x_to_point": x_to_point_2d,
            "group": grp,
            "halo": obs_glow_2d,
            "galaxy_updater_2d": galaxy_updater_2d,
        }

    # ------------------------
    #        1D MODULAIRE
    # ------------------------
    def _1d_setup(
        self,
        x_min=-24,
        x_max=23,
        sprite_size=0.22,
        halo_radius=0.4,
        halo_width=2.5,
        show_vectors_default=False,
    ):
        # State container
        self._one_d = getattr(self, "_one_d", {})
        od = self._one_d

        # Galaxies sur une ligne comobile
        x0s = list(range(int(x_min), int(x_max) + 1))
        galaxies = []
        for x0 in x0s:
            g = make_galaxy_img(size=sprite_size)
            g._x0 = float(x0)
            g.set_opacity(0.0)
            g.set_z_index(Z_GALAXY)
            galaxies.append(g)
        self.add(*galaxies)

        # Trackers
        s = mn.ValueTracker(1.0)   # facteur d'échelle
        r = mn.ValueTracker(0.0)   # observateur (translation interne)
        od["s"], od["r"] = s, r
        od["x0s"] = x0s
        od["galaxies"] = galaxies

        # Mapping (largeur virtuelle pour conserver les trucs en cadre)
        x_min_map, x_max_map = -10.0, 10.0
        VIRTUAL_SCALE = 3.0
        center = self.anim_zone.get_center()
        unit_px = (self.anim_zone.width * VIRTUAL_SCALE) / (x_min_map - x_max_map)

        def x_to_point(x: float) -> np.ndarray:
            return center + np.array([x * unit_px, 0.0, 0.0])

        def galaxy_updater(m: mn.Mobject):
            x = (m._x0 - r.get_value()) * s.get_value()
            m.move_to(x_to_point(x))

        od["x_to_point"] = x_to_point
        od["galaxy_updater"] = galaxy_updater

        for g in galaxies:
            g.add_updater(galaxy_updater)

        # Halo observateur initial (x0=0)
        obs_glow = mn.Circle(radius=halo_radius).set_stroke(OBS, width=halo_width)
        obs_glow.set_z_index(Z_HALO)

        def update_glow(m):
            nearest = min(galaxies, key=lambda gg: abs(gg._x0 - r.get_value()))
            m.move_to(nearest.get_center())

        obs_glow.add_updater(update_glow)
        self.add(obs_glow)
        od["obs_glow"] = obs_glow

        # Vecteurs de vitesse (optionnels) — garde Vector, corrige le sens
        od["vec_vis"] = mn.ValueTracker(1.0 if show_vectors_default else 0.0)
        od["hide_obs_vec"] = mn.ValueTracker(1.0)  # cache le vecteur de l'observateur
        velocity_vectors = []

        def make_velocity_vector(gal: mn.Mobject):
            vec = mn.Vector([0.001, 0, 0], color=VEC_COLOR, stroke_width=3.0, tip_length=0.25)
            vec.set_z_index(Z_VECTOR).set_opacity(0.0)

            def vec_updater(m: mn.Vector):
                base_opa = od["vec_vis"].get_value()
                is_obs = (abs(gal._x0 - r.get_value()) < 1e-6)
                opa = 0.0 if (is_obs and od["hide_obs_vec"].get_value() >= 0.5) else base_opa

                d_phys = abs(gal._x0 - r.get_value()) * s.get_value()
                L = min(1.0, 0.10 + 0.18 * d_phys)

                # ---- direction corrigée : pointe vers l'extérieur ----
                dir_vec = np.array([-1.0 if (gal._x0 - r.get_value()) >= 0 else 1.0, 0.0, 0.0])

                new_vec = mn.Vector(dir_vec * L, color=VEC_COLOR, stroke_width=3.0, tip_length=0.25).set_opacity(opa)
                new_vec.move_to(gal.get_center() + np.array([0.0, 0.35, 0.0]))
                new_vec.set_z_index(Z_VECTOR)
                m.become(new_vec)

            vec.add_updater(vec_updater)
            return vec

        for gal in galaxies:
            velocity_vectors.append(make_velocity_vector(gal))
        self.add(*velocity_vectors)

        grp = mn.Group(*galaxies, *velocity_vectors, obs_glow)
        grp.set_z_index(Z_GROUP)
        self._center_group = grp

        od["velocity_vectors"] = velocity_vectors

        # Apparition des galaxies (pas de FadeIn global pour éviter clignotement)
        self.play(*[g.animate.set_opacity(1.0) for g in galaxies], run_time=0.5)
        # Petit pulse halo
        self.play(mn.Indicate(obs_glow, scale_factor=1.05), run_time=0.4)

    def _1d_show_vectors(self, visible=True, rt=0.35):
        od = self._one_d
        target = 1.0 if visible else 0.0
        self.play(od["vec_vis"].animate.set_value(target), run_time=rt)

    def _1d_expand(self, factor=2.2, rt=1.2):
        od = self._one_d
        self.play(od["s"].animate.set_value(factor), run_time=rt, rate_func=mn.rate_functions.ease_in_out_sine)

    def _1d_reset(self, rt=0.8, hide_vectors_during=True):
        od = self._one_d
        if hide_vectors_during:
            self.play(od["vec_vis"].animate.set_value(0.0), run_time=0.25)
        self.play(od["s"].animate.set_value(1.0), run_time=rt, rate_func=mn.rate_functions.ease_in_out_sine)
        if hide_vectors_during:
            self.play(od["vec_vis"].animate.set_value(1.0), run_time=0.25)

    def _1d_change_observer(self, new_x=2.0, rt=1.1):
        od = self._one_d
        self.play(od["hide_obs_vec"].animate.set_value(0.0), run_time=0.15)
        self.play(od["r"].animate.set_value(new_x), run_time=rt, rate_func=mn.rate_functions.ease_in_out_sine)
        self.play(od["hide_obs_vec"].animate.set_value(1.0), run_time=0.15)
        self.play(mn.Indicate(od["obs_glow"], scale_factor=1.05), run_time=0.4)

    def _1d_cleanup(self, rt=0.4):
        od = getattr(self, "_one_d", {})
        for g in od.get("galaxies", []):
            for u in list(g.updaters):
                g.remove_updater(u)
        for v in od.get("velocity_vectors", []):
            v.clear_updaters()
        if od.get("obs_glow") is not None:
            od["obs_glow"].clear_updaters()

        if getattr(self, "_center_group", None) is not None:
            try:
                self.play(mn.FadeOut(self._center_group), run_time=rt)
            except Exception:
                pass
            self.remove(self._center_group)
            self._center_group = None

        self._one_d = {}

    # ------------------------
    #         SCÈNE
    # ------------------------
    def construct(self):
        self.camera.background_color = BG
        self.setup_layout()
        
        show_expansion_title_card(
            self,
            title_text=t("title"),
            image_path="deepfield.png",
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
            hold=1,
        )

        chap0 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[],
        )
        self.show_chapter(chap0)

        # ---------- 2D standalone AVANT chapitres ----------
        self.setup_expansion_2d()

        # ---------- Chapitre 1 : texte seul (2D reste affichée) ----------
        chap1 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence01"),
                t("sentence02"),
                {"type": "text", "content": t("sentence03"), "anim": lambda s, l: s.play_expansion_only(), "pause": 1},
                t("sentence04"),
                t("sentence05"),
                t("sentence06"),
                t("sentence07"),
            ],
        )
        self.show_chapter(chap1)
        self.wait(2.0)

        # ---------- Début Chapitre 2 : FadeOut 2D ----------
        if getattr(self, "_center_group", None) is not None:
            self.play(mn.FadeOut(self._center_group, run_time=0.8))
            self.remove(self._center_group)
            self._center_group = None


        # ---------- Chapitre 2 : 1D modulaire + texte intercalé ----------
        chap2 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence11"),
                {"type": "text", "content": t("sentence12"), "anim": lambda s, l: s._1d_setup(show_vectors_default=False), "pause": 2},
                {"type": "text", "content": t("sentence13"), "anim": lambda s, l: s._1d_show_vectors(True), "pause": 2},
                {"type": "text", "content": t("sentence14")},
                {"type": "text", "content": t("sentence15"), "anim": lambda s, l: s._1d_expand(factor=2.2, rt=2.6), "pause": 2},
                {"type": "text", "content": t("sentence16"), "anim": lambda s, l: s._1d_reset(rt=0.8, hide_vectors_during=True), "pause": 1},
                {"type": "text", "content": t("sentence17"), "anim": lambda s, l: s._1d_change_observer(new_x=-8.0, rt=4.6), "pause": 1},
                {"type": "text", "content": t("sentence18")},
                {"type": "text", "content": t("sentence19"), "anim": lambda s, l: s._1d_expand(factor=2.2, rt=2.6), "pause_before":1},
                ],
        )
        self.show_chapter(chap2)
        self.wait(2.0)

        self._1d_cleanup(rt=0.8)
        self.clear_text(bottom_only=True)

        # ---------- Remplacer par une image fixe (par ex. une texture PNG) ----------
        img = mn.ImageMobject("deepfield.png").scale(0.4)  # ton image
        img.set_z_index(Z_GROUP)
        img.scale_to_fit_height(self.anim_zone.height * 0.9)
        img.move_to(self.anim_zone.get_center())
        self.play(mn.FadeIn(img, run_time=1.0))
        self._center_group = img  # pour que clear_text puisse la gérer


        chap3 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence21"),
                t("sentence22"),
                {"type": "text", "content": t("sentence23"), "pause": 2},
                t("sentence24"),
                t("sentence25"),
            ],
        )
        self.show_chapter(chap3)
        self.wait(3.0)
        # CTA
        cta = mn.Text(t("cta_sub"), color=mn.RED).scale(0.5)
        cta.set_z_index(30)
        cta.next_to(self._title_current, mn.DOWN, buff=0.3)
        title_group = mn.Group(self._title_current, cta)
        title_group.set_z_index(30)
        self._title_current = title_group

        self.wait(2.0)
        self.play(mn.FadeIn(cta, shift=mn.DOWN*0.2), run_time=0.9)
        self.wait(3.0)

        # Nettoyage final
        self.clear_text(clear_figure=True)
