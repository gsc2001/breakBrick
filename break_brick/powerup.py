from typing import List

from colorama import Fore, Style
import numpy as np

import config
from .ball import Ball
from .objects import AutoMovingObject, GameObject
from .graphics import *
from .paddle import Paddle


class PowerUp(AutoMovingObject):
    """Base class for all the power ups"""

    def __init__(self, rep, pos, color, vel=np.array([0, config.POWERUP_SPEED])):
        super().__init__(rep, pos, color, vel)
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

    def update(self):
        _, _y_vel = self.get_velocity()
        self.set_yvelocity(_y_vel + config.GRAVITY)
        super().update()

    def add_time(self, time):
        self._time_left += time

    def get_time(self):
        return self._time_left

    def __str__(self):
        if not self._activated:
            return self.__class__.__name__ + ' Not activated'
        return self.__class__.__name__ + ' ' + str(self._time_left)


class ExpandPaddle(PowerUp):
    """The expand paddle powerup"""

    def __init__(self, pos, *args):
        rep = GameObject.rep_from_str(EXPAND_PADDLE)
        color = np.array(["", Fore.YELLOW + Style.BRIGHT])
        super().__init__(rep, pos, color, *args)

    def activate(self, paddle: Paddle):
        _, _width = paddle.get_shape()
        paddle.set_width(_width + config.PADDLE_CHANGE_AMT)
        super().activate()

    def deactivate(self, paddle: Paddle):
        _, _width = paddle.get_shape()
        paddle.set_width(_width - config.PADDLE_CHANGE_AMT)
        super().deactivate()


class ShrinkPaddle(PowerUp):
    """Shrink paddle powerup"""

    def __init__(self, pos, *args):
        rep = GameObject.rep_from_str(SHRINK_PADDLE)
        color = np.array(["", Fore.YELLOW + Style.BRIGHT])
        super().__init__(rep, pos, color, *args)

    def activate(self, paddle: Paddle):
        _, _width = paddle.get_shape()
        paddle.set_width(_width - config.PADDLE_CHANGE_AMT)
        super().activate()

    def deactivate(self, paddle: Paddle):
        _, _width = paddle.get_shape()
        paddle.set_width(_width + config.PADDLE_CHANGE_AMT)
        super().deactivate()


class FastBall(PowerUp):
    """Fast ball PowerUp"""

    def __init__(self, pos, *args):
        rep = GameObject.rep_from_str(FAST_BALL)
        color = np.array(["", Fore.YELLOW + Style.BRIGHT])
        super().__init__(rep, pos, color, *args)

    def activate(self, balls: List[Ball]):
        for ball in balls:
            _x_vel, _y_vel = ball.get_velocity()
            ball.set_xvelocity(config.FAST_BALL_MULTIPLIER * _x_vel)
            ball.set_yvelocity(config.FAST_BALL_MULTIPLIER * _y_vel)
        super().activate()

    def deactivate(self, balls: List[Ball]):
        for ball in balls:
            _x_vel, _y_vel = ball.get_velocity()
            ball.set_xvelocity(_x_vel / config.FAST_BALL_MULTIPLIER)
            ball.set_yvelocity(_y_vel / config.FAST_BALL_MULTIPLIER)
        super().deactivate()


class BallMultiplier(PowerUp):
    """Ball multiplier powerup"""

    def __init__(self, pos, *args):
        rep = GameObject.rep_from_str(BALL_MULTIPLIER)
        color = np.array(["", Fore.YELLOW + Style.BRIGHT])
        super().__init__(rep, pos, color, *args)

    def reduce_time(self):
        """This powerup never dies"""
        return False

    def activate(self, balls: List[Ball]):
        new_balls = []
        for ball in balls:
            if ball.is_sticked():
                new_ball = Ball(ball.get_position(), np.array([1, -1]))
                new_balls.append(new_ball)
            else:
                vel = ball.get_velocity()
                new_ball = Ball(ball.get_position(), vel + np.array([-1, 0]))
                ball.set_xvelocity(vel[0] + 1)
                new_balls.append(new_ball)
        super().activate()
        return new_balls


class ThruBall(PowerUp):
    """ThruBall Powerup"""

    def __init__(self, pos, *args):
        rep = GameObject.rep_from_str(THRU_BALL)
        color = np.array(["", Fore.YELLOW + Style.BRIGHT])
        super().__init__(rep, pos, color, *args)

    def activate(self, *objs):
        super().activate()
        return True  # just need to set _thru_balls variable to True

    def deactivate(self, *objs):
        super().deactivate()
        return False  # just need to set _thru_balls variable to False


class PaddleGrab(PowerUp):
    """PaddleGrab Powerup"""

    def __init__(self, pos, *args):
        rep = GameObject.rep_from_str(PADDLE_GRAB)
        color = np.array(["", Fore.YELLOW + Style.BRIGHT])
        super().__init__(rep, pos, color, *args)

    def activate(self, paddle: Paddle):
        paddle.set_sticky(True)
        super().activate()

    def deactivate(self, paddle: Paddle):
        paddle.set_sticky(False)
        super().deactivate()


class ShootingPaddle(PowerUp):
    """Shooting paddle powerup"""

    def __init__(self, pos, *args):
        rep = GameObject.rep_from_str(SHOOTING_PADDLE)
        color = np.array(["", Fore.YELLOW + Style.BRIGHT])
        super().__init__(rep, pos, color, *args)

    def activate(self, paddle: Paddle):
        paddle.shoot_bullets()
        super().activate()
        return True

    def deactivate(self, paddle: Paddle):
        paddle.stop_shooting()
        super().deactivate()
        return False
