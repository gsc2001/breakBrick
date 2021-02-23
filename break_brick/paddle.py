import colorama
import numpy as np

import config
from .objects import GameObject
from .ball import Ball


class Paddle(GameObject):

    def __init__(self):
        rep = np.full((1, config.PADDLE_WIDTH_NORMAL), "=")
        color = np.array([colorama.Back.WHITE, colorama.Fore.WHITE])

        super().__init__(rep, np.array([config.WIDTH // 2 - config.PADDLE_WIDTH_NORMAL // 2, config.HEIGHT - 2]),
                         color)

        self._width = config.PADDLE_WIDTH_NORMAL
        self._sticky = False
        self._stick_ball = None

    def move_left(self):
        """Move paddle to left"""
        self.set_position(self.get_position() - [config.PADDLE_SPEED, 0])
        if self._stick_ball is not None:
            _pos = self._stick_ball.get_position()
            self._stick_ball.set_position(_pos - [config.PADDLE_SPEED, 0])

    def move_right(self):
        """Move paddle to right"""
        self.set_position(self.get_position() + [config.PADDLE_SPEED, 0])
        if self._stick_ball is not None:
            _pos = self._stick_ball.get_position()
            self._stick_ball.set_position(_pos + [config.PADDLE_SPEED, 0])

    def get_middle(self):
        """Get middle of the paddle"""
        return self.get_position()[0] + self._width // 2

    def set_width(self, width: int):
        """Set the paddle width to `width`"""
        self._width = width
        self.set_rep(np.full((1, self._width), "="))

    def set_sticky(self, sticky):
        self._sticky = sticky
        if not sticky:
            self.remove_ball()

    def is_sticky(self):
        return self._sticky and (self._stick_ball is None)

    def stick_ball(self, ball: Ball):
        self._stick_ball = ball
        ball.stick_to_paddle()

    def remove_ball(self):
        if self._stick_ball is None:
            return
        self._stick_ball.leave_paddle()
        self._stick_ball = None
