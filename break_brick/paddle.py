import colorama
import numpy as np

import config
from .objects import GameObject


class Paddle(GameObject):

    def __init__(self):
        rep = np.full((1, config.PADDLE_WIDTH_NORMAL), "=")
        color = np.array([colorama.Back.WHITE, colorama.Fore.WHITE])

        super().__init__(rep, np.array([int(config.WIDTH / 2 - config.PADDLE_WIDTH_NORMAL / 2 + 1), config.HEIGHT - 2]),
                         color)

        self._width = config.PADDLE_WIDTH_NORMAL

    def move_left(self):
        """Move paddle to left"""
        self.set_position(self.get_position() - [config.PADDLE_SPEED, 0])

    def move_right(self):
        """Move paddle to right"""
        self.set_position(self.get_position() + [config.PADDLE_SPEED, 0])
