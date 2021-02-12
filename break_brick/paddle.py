import colorama
import numpy as np

import config
from .objects import GameObject


class Paddle(GameObject):

    def __init__(self):
        rep = np.full((1, config.PADDLE_WIDTH_NORMAL), "=")
        color = np.array([colorama.Back.WHITE, colorama.Fore.WHITE])

        super().__init__(rep, np.array([config.WIDTH / 2, config.HEIGHT - 2]), color)

        self._width = config.PADDLE_WIDTH_NORMAL

    def move_left(self):
        """Move paddle to left"""
        self._pos[0] -= config.PADDLE_SPEED
        self._pos[0] = max(0, self._pos[0])

    def move_right(self):
        """Move paddle to right"""
        self._pos[0] += config.PADDLE_SPEED
        self._pos[0] = min(config.WIDTH - 1 - self._width, self._pos[0])
