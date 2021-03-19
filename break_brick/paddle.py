import colorama
import numpy as np

import config
from .objects import GameObject
from .ball import Ball


class Paddle(GameObject):

    def __init__(self):
        rep = np.full((1, config.PADDLE_WIDTH_NORMAL), "=")
        color = np.array([colorama.Back.WHITE, colorama.Fore.WHITE])

        super().__init__(rep, np.array([config.WIDTH // 2 - config.PADDLE_WIDTH_NORMAL // 2, config.HEIGHT - 4]),
                         color)

        self._width = config.PADDLE_WIDTH_NORMAL
        self._sticky = False
        self._shooting = False
        self._stick_ball = None

    def move_left(self):
        """Move paddle to left"""
        set = self.set_position(self.get_position() - [config.PADDLE_SPEED, 0])
        if self._stick_ball is not None and set:
            _pos = self._stick_ball.get_position()
            self._stick_ball.set_position(_pos - [config.PADDLE_SPEED, 0])

    def move_right(self):
        """Move paddle to right"""
        set = self.set_position(self.get_position() + [config.PADDLE_SPEED, 0])
        if self._stick_ball is not None and set:
            _pos = self._stick_ball.get_position()
            self._stick_ball.set_position(_pos + [config.PADDLE_SPEED, 0])

    def get_middle(self):
        """Get middle of the paddle"""
        _x, _y = self.get_position()
        return np.array([_x + self._width // 2, _y])

    def set_width(self, width: int):
        """Set the paddle width to `width`"""
        self._width = np.clip(width, config.PADDLE_WIDTH_MIN, config.PADDLE_WIDTH_MAX)
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

    def shoot_bullets(self):
        if config.DEBUG:
            assert not self._shooting
        self._shooting = True
        self.set_color(np.array([colorama.Back.RED, colorama.Fore.RED]))

    def stop_shooting(self):
        if config.DEBUG:
            assert self._shooting
        self._shooting = False
        self.set_color(np.array([colorama.Back.WHITE, colorama.Fore.WHITE]))
