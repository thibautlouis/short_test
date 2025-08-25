# frame_sequence_player.py
from manim import *
import glob
import numpy as np

class FrameSequencePlayer(ImageMobject):
    """
    Joue une séquence d'images comme une vidéo, mais contrôlable :
    - play(), pause()
    - goto_time(t)
    - step(frames)
    - loop True/False
    Confiné dans une zone max_w x max_h, centré en 'center'.
    """
    def __init__(self, pattern, fps=30, center=ORIGIN, max_w=6.0, max_h=6.0,
                 loop=False, z=10, autoplay=True):
        files = sorted(glob.glob(pattern))
        assert files, f"Aucune image trouvée pour {pattern}"
        self.files = files
        self.fps = fps
        self.dt_per = 1.0 / fps
        self.loop = loop
        self.playing = autoplay

        self.idx = 0
        self.t = 0.0  # temps courant en secondes

        super().__init__(files[0])
        self.set_z_index(z)

        self._center = np.array(center)
        self._max_w = float(max_w)
        self._max_h = float(max_h)

        self._apply_fit()

        def _upd(mobj: "FrameSequencePlayer", dt: float):
            if not self.playing:
                return
            self.t += dt
            while self.t >= self.dt_per and (self.loop or self.idx < len(self.files)-1):
                self.t -= self.dt_per
                self.idx = (self.idx + 1) % len(self.files) if self.loop else min(self.idx + 1, len(self.files)-1)
                self._show_frame()

        self.add_updater(_upd)

    # === API de contrôle ===
    def play(self): self.playing = True
    def pause(self): self.playing = False

    def goto_time(self, t_sec: float):
        """Positionne à un temps absolu (en secondes)"""
        idx = int(round(t_sec * self.fps))
        if not self.loop:
            idx = max(0, min(idx, len(self.files)-1))
        else:
            idx = idx % len(self.files)
        self.idx = idx
        self.t = 0.0
        self._show_frame()

    def step(self, frames: int = 1):
        """Avance/recul de N frames"""
        self.idx = (self.idx + frames) % len(self.files) if self.loop else max(0, min(self.idx + frames, len(self.files)-1))
        self._show_frame()

    # === internes ===
    def _show_frame(self):
        self.become(ImageMobject(self.files[self.idx]).set_z_index(self.z_index))
        self._apply_fit()

    def _apply_fit(self):
        s = min(self._max_w / self.width, self._max_h / self.height)
        self.scale(s)
        self.move_to(self._center)
