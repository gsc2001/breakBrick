from colorama import Fore, Back, Style
import numpy as np

import config
from .objects import AutoMovingObject, GameObject
from .graphics import *
from .paddle import Paddle


class PowerUp(AutoMovingObject):
    """Base class for all the power ups"""

    def __init__(self, rep, pos, color):
        super().__init__(rep, pos, color, np.array([0, config.POWERUP_SPEED]))
        self._time_left = config.POWERUP_FRAMES
        self._activated = False

    def activate(self, *objs):
        """Activate the powerup"""
        self._activated = True

    def deactivate(self, *objs):
        """Deactivate the powerup"""
        self._activated = False
        self.destroy()

    def reduce_time(self):
        self._time_left -= 1

        if self._time_left == 0:
            return True

        return False

    def is_falling(self):
        return not self._activated and self.is_active()

    def is_activated(self):
        return self._activated

    def handle_wall_collision(self):
        _h, _ = self.get_shape()
        _, _y = self.get_position()

        if int(_y + _h) == config.HEIGHT - 1:
            self.destroy()


class ExpandPaddle(PowerUp):
    """The expand paddle powerup"""

    def __init__(self, pos):
        rep = GameObject.rep_from_str(EXPAND_PADDLE)
        color = np.array(["", Fore.YELLOW + Style.BRIGHT])
        self._paddle = None
        super().__init__(rep, pos, color)

    def activate(self, paddle: Paddle):
        paddle.set_width(config.PADDLE_WIDTH_LONG)
        super().activate()

    def deactivate(self, paddle: Paddle):
        paddle.set_width(config.PADDLE_WIDTH_NORMAL)
        super().deactivate()
