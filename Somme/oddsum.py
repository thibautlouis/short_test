import manim as mn
import numpy as np
import manim_helper as mh
from oddsum_lang import t, LANG
from oddsum_title_card import show_title_card


# --- 9:16 ---
mn.config.frame_width  = 9
mn.config.frame_height = 16
mn.config.pixel_width  = 1080
mn.config.pixel_height = 1920

BG = mn.BLACK
LINE_COLOR  = "#FFD700"   # "#FFFFFF" si tu préfères
GRID_STROKE = 2


class OddSumShort(mh.TextChaptersScene):
    # ---------- helpers grille ----------
    def _build_edges_world(self, n_max=6, cell=1.0):
        """
        Construit tous les segments d'une grille n_max×n_max, masqués (stroke opacity=0).
        Renvoie (edges, world) et place world dans self.anim_zone.
        """
        edges = {}
        lines = []

        # horizontaux H(r,c): (c,r)->(c+1,r)
        for r in range(n_max + 1):
            for c in range(n_max):
                p1 = np.array([c*cell,     r*cell, 0.0])
                p2 = np.array([(c+1)*cell, r*cell, 0.0])
                ln = mn.Line(p1, p2, stroke_width=GRID_STROKE)
                ln.set_color(LINE_COLOR).set_stroke(opacity=0.0)
                edges[("H", r, c)] = ln
                lines.append(ln)

        # verticaux V(r,c): (c,r)->(c,r+1)
        for c in range(n_max + 1):
            for r in range(n_max):
                p1 = np.array([c*cell, r*cell,     0.0])
                p2 = np.array([c*cell, (r+1)*cell, 0.0])
                ln = mn.Line(p1, p2, stroke_width=GRID_STROKE)
                ln.set_color(LINE_COLOR).set_stroke(opacity=0.0)
                edges[("V", r, c)] = ln
                lines.append(ln)

        world = mn.VGroup(*lines)
        mh.fit_into(world, self.anim_zone, pad=0.80)   # contraint à la zone FIGURE
        self.add(world)
        return edges, world

    def _edge_keys_for_k(self, k: int):
        keys = set()
        for r in range(k + 1):
            for c in range(k):
                keys.add(("H", r, c))
        for c in range(k + 1):
            for r in range(k):
                keys.add(("V", r, c))
        return keys

    def _reveal_k(self, k: int, edges, visible: set, run_time=0.6):
        """Révèle les segments nécessaires pour afficher le carré k×k."""
        want = self._edge_keys_for_k(k)
        new_keys = sorted(list(want - visible))
        if not new_keys:
            return
        anims = [edges[key].animate.set_stroke(opacity=1.0) for key in new_keys]
        self.play(*anims, run_time=run_time)
        visible |= set(new_keys)

    # ---------- somme affichée (ancrage + tokens) ----------
    def _sum_guides(self, world: mn.VGroup, n_max: int, y_offset_factor=0.3, min_clear=0.0):
        """
        Calcule:
        - des ancres (points invisibles) centrées sous chaque colonne et entre colonnes
        - positions sûres DANS la zone figure (clamp pour rester visibles)
        """
        left_x   = world.get_left()[0]
        bottom_y = world.get_bottom()[1]
        dx = world.width / n_max

        # position cible "juste sous la grille"
        y_pref = bottom_y - y_offset_factor * dx
        # clamp au-dessus du bord bas de la zone anim (avec marge)
        az_bot = self.anim_zone.get_bottom()[1]
        y_min  = az_bot + min_clear * dx
        y = max(y_pref, y_min)

        # ancres: une par colonne (termes), et une entre colonnes (plus)
        term_anchors = []
        plus_anchors = []
        for k in range(1, n_max + 1):
            ax = left_x + (k - 0.5) * dx
            term_anchors.append(mn.Dot([ax, y, 0], radius=0.001, color=mn.BLACK, fill_opacity=0))
            if k >= 2:
                axp = left_x + (k - 1.0) * dx
                plus_anchors.append(mn.Dot([axp, y, 0], radius=0.001, color=mn.BLACK, fill_opacity=0))

        term_anchor_group = mn.VGroup(*term_anchors)
        plus_anchor_group = mn.VGroup(*plus_anchors) if plus_anchors else mn.VGroup()
        # on les ajoute pour qu'ils suivent la même éventuelle transformation que world (via _center_group)
        self.add(term_anchor_group, plus_anchor_group)

        return term_anchor_group, plus_anchor_group, dx

    def _oddsum_setup(self, n_max=6, tok_scale=0.60):
        """
        Prépare la grille + les ancres + crée tous les tokens ('1 + 3 + 5 + ...') masqués.
        """
        # Si déjà prêt avec même n_max, ne rien faire
        if getattr(self, "_oddsum", None) and self._oddsum.get("n_max") == n_max:
            return

        # Nettoie l'ancien état si présent
        if getattr(self, "_oddsum", None):
            grp = self._oddsum.get("group", None)
            if grp is not None:
                self.remove(grp)

        edges, world = self._build_edges_world(n_max, cell=1.0)
        visible = set()

        # Ancres sous la grille
        term_anchors, plus_anchors, dx = self._sum_guides(world, n_max)
        tok_color = LINE_COLOR

        terms = {}
        pluses = {}
        mlist  = []

        # Crée les tokens (MathTex), masqués, placés sur les ancres
        t1 = mn.MathTex("1").set_color(tok_color).scale(tok_scale)
        t1.move_to(term_anchors[0]).set_opacity(0.0)
        terms[1] = t1
        mlist.append(t1)

        for k in range(2, n_max + 1):
            pl = mn.MathTex("+").set_color(tok_color).scale(tok_scale)
            pl.move_to(plus_anchors[k-2]).set_opacity(0.0)
            pluses[k] = pl
            mlist.append(pl)

            tm = mn.MathTex(f"{2*k-1}").set_color(tok_color).scale(tok_scale)
            tm.move_to(term_anchors[k-1]).set_opacity(0.0)
            terms[k] = tm
            mlist.append(tm)

        tok_group = mn.VGroup(*mlist).set_z_index(100)
        # Regroupe tout pour que les transformations de chapitre s'appliquent d'un bloc
        group = mn.VGroup(world, term_anchors, plus_anchors, tok_group).set_z_index(5)

        self.add(tok_group)   # visibles (mais opacité 0), présents dans la scène
        self._center_group = group
        self._oddsum = {
            "n_max": n_max,
            "edges": edges,
            "world": world,
            "visible": visible,
            "terms": terms,
            "pluses": pluses,
            "tok_group": tok_group,
            "group": group,
        }

    def _oddsum_reveal(self, k: int, gap=0.16, hold=0.30,
                       write_rt_first=0.35, edge_rt_first=0.45,
                       write_rt=0.40, edge_rt=0.70):
        """
        Étape k: écrire le terme sous la grille (Write) + révéler la couche k×k.
        """
        st = self._oddsum

        if k == 1:
            # Rendre visible le 1 et l'écrire
            st["terms"][1].set_opacity(1.0)
            self.play(mn.Write(st["terms"][1]), run_time=write_rt_first)
            self._reveal_k(1, st["edges"], st["visible"], run_time=edge_rt_first)
            self.wait(hold)
            return

        anims = []
        if k in st["pluses"]:
            st["pluses"][k].set_opacity(1.0)
            anims.append(mn.Write(st["pluses"][k]))
        if k in st["terms"]:
            st["terms"][k].set_opacity(1.0)
            anims.append(mn.Write(st["terms"][k]))
        if anims:
            self.play(*anims, run_time=write_rt)

        self._reveal_k(k, st["edges"], st["visible"], run_time=edge_rt)
        self.wait(gap)

    def _oddsum_step(self, k: int, n_max=6, **timings):
        self._oddsum_setup(n_max=n_max)
        self._oddsum_reveal(k, **timings)

    # ---------- Scene ----------
    def construct(self):
    
        show_title_card(
            self,
            title_text=t("title"),
            formula_tex=r"1 + 3 + 5 + 7 + 9 + .....",
            logo_path="/Users/louisthibaut/Desktop/projects/math_video/logo/astramath.png",
            hold=2,
        )
        
        self.camera.background_color = BG
        self.setup_layout()

        # Titre seul
        chap0 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[]
        )
        self.show_chapter(chap0)
        
        
        # (Optionnel) Une image d'intro si tu en as une
        img = mn.ImageMobject("principia_new.png").scale(0.4)
        img.scale_to_fit_height(self.anim_zone.height * 0.9)
        img.move_to(self.anim_zone.get_center())
        self.play(mn.FadeIn(img, run_time=1.0))
        self._center_group = img


        # Chapitre d'intro (phrases)
        chap1 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence01"),
                t("sentence02"),
                t("sentence03"),
                {"type": "text", "content":  t("sentence04"), "pause": 2},
                {"type": "text", "content":  t("sentence05")},
            ]
        )
        self.show_chapter(chap1)
        self.wait(4.0)
        self.clear_text(bottom_and_figure=True)

        # Chapitre 2 : construction visuelle + somme alignée sous la grille
        chap2 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
            
                t("sentence11"),
                t("sentence12"),

                {"type": "text", "content": t("sentence13")["content"],
                 "anim": lambda scene, m: (
                     scene._oddsum_step(1, n_max=4, write_rt_first=0.30, edge_rt_first=0.35, hold=0.45),
                     scene.clear_text(bottom_only=True)
                 )},
                {"type": "text", "content": t("sentence14")["content"],
                 "anim": lambda scene, m: (
                     scene._oddsum_step(2, n_max=4, write_rt=0.28, edge_rt=0.45, gap=1, hold=0.45),
                     scene.clear_text(bottom_only=True)
                 )},
                {"type": "text", "content": t("sentence15")["content"],
                 "anim": lambda scene, m: (
                     scene._oddsum_step(3, n_max=4, write_rt=0.28, edge_rt=0.45, gap=1, hold=0.45),
                     scene.clear_text(bottom_only=True)
                 )},
                {"type": "text", "content": t("sentence16"),
                 "anim": lambda scene, m: (
                     scene._oddsum_step(4, n_max=4, write_rt=0.20, edge_rt=0.30, gap=2),
                     scene.clear_text(bottom_only=True)
                 )},
                t("sentence17"),
                t("sentence18"),

            ],
        )
        self.show_chapter(chap2)
        self.wait(4.0)
        self.clear_text(bottom_only=True)


        chap3 = mh.ChapterText(
            title=t("title"),
            bottom_lines=[
                t("sentence21"),
                t("sentence22"),
                t("sentence23"),
                {"type": "text", "content":  t("sentence24"), "pause": 1},
                {"type": "text", "content":  t("sentence25"), "pause": 3},
                {"type": "text", "content":  t("sentence26"), "pause": 1},
                {"type": "text", "content":  t("sentence27"), "pause": 3},
                t("sentence28"),
                t("sentence29"),
            ]
        )
        self.show_chapter(chap3)
        self.wait(4.0)
        # CTA
        cta = mn.Text(t("cta_sub"), color=mn.RED).scale(0.5)
        cta.set_z_index(30)
        cta.next_to(self._title_current, mn.DOWN, buff=0.3)
        title_group = mn.Group(self._title_current, cta)
        title_group.set_z_index(30)
        self._title_current = title_group

        self.play(mn.FadeIn(cta, shift=mn.DOWN*0.2), run_time=0.9)
        self.wait(3.0)

        # Nettoyage final
        self.clear_text(clear_figure=True)
