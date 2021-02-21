import colorama
import numpy as np

import config
from .objects import GameObject


class Paddle(GameObject):

    def __init__(self):
        rep = np.full((1, config.PADDLE_WIDTH_NORMAL), "=")
        color = np.array([colorama.Back.WHITE, colorama.Fore.WHITE])

        super().__init__(rep, np.array([config.WIDTH // 2 - config.PADDLE_WIDTH_NORMAL // 2, config.HEIGHT - 2]),
                         color)

        self._width = config.PADDLE_WIDTH_NORMAL

    def move_left(self):
        """Move paddle to left"""
        self.set_position(self.get_position() - [config.PADDLE_SPEED, 0])

    def move_right(self):
        """Move paddle to right"""
        self.set_position(self.get_position() + [config.PADDLE_SPEED, 0])

    def get_middle(self):
        """Get middle of the paddle"""
        return self.get_position()[0] + self._width // 2

    def set_width(self, width: int):
        """Set the paddle width to `width`"""
        self._width = width
        self.set_rep(np.full((1, self._width), "="))
