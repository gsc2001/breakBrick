import colorama
import numpy as np

import config
import break_brick.utils as utils
from .objects import AutoMovingObject, GameObject
from .graphics import BALL


class Ball(AutoMovingObject):
    """
    Class for the ball
    """

    def __init__(self, pos=None, vel=None):
        rep = GameObject.rep_from_str(BALL)
        color = np.array([config.BG_COLOR, colorama.Fore.WHITE + colorama.Style.BRIGHT])
        if pos is None:
            pos = np.array([int(config.WIDTH / 2), config.HEIGHT - 5])
        if vel is None:
            vel = np.array([0, config.BALL_SPEED_NORMAL])
        # self._thru = False
        # if the ball is sticked to the paddle
        self._sticked = False
        self._stored_velocity = vel
        super().__init__(rep, pos, color, vel)

    def handle_paddle_collision(self, paddle_middle, paddle_width):
        """Handle collision with paddle"""
        _x, _y = self.get_position()
        _x_vel, _y_vel = self.get_velocity()
        self.handle_collision(x_collision=False, y_collision=True)
        self.set_position(np.array([_x, _y - 1]))

        if abs(_y_vel) < 0.1:
            self.set_yvelocity(-0.2)

        self.set_xvelocity(_x_vel + int(_x - paddle_middle) / paddle_width)

    def handle_brick_collision(self, x_collision, y_collision, thru_ball: bool):
        if not thru_ball:
            self.handle_collision(x_collision, y_collision)

    def stick_to_paddle(self):
        self._sticked = True
        self._stored_velocity = self.get_velocity()
        self.set_xvelocity(0)
        self.set_yvelocity(0)

    def leave_paddle(self):
        self._sticked = False
        self.set_xvelocity(self._stored_velocity[0])
        self.set_yvelocity(self._stored_velocity[1])

    def is_sticked(self):
        return self._sticked
    # def set_thru(self, thru: bool):
    #     """Make a ball thru or remove"""
    #     self._thru = thru
    #
    # def is_thru(self) -> bool:
    #     """Get if ball is thru"""
    #     return self._thru
