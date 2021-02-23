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
        self._stored_velocity = np.array([0.0, 0.0])
        super().__init__(rep, pos, color, vel)

    def handle_collision(self, x_collision, y_collision):
        """
        Handle collision
        :param x_collision: was the collsion in x
        :param y_collision: was the collision in y
        :return:
        """
        _x_vel, _y_vel = self.get_velocity()
        if x_collision:
            self.set_xvelocity(-_x_vel)
            self.set_position(self._pos + np.array([np.sign(-_x_vel), 0]))

        if y_collision:
            self.set_yvelocity(-_y_vel)
            self.set_position(self._pos + np.array([0, np.sign(-_y_vel)]))

    def handle_wall_collision(self) -> bool:
        """
        Handle ball collision with wall
        :return: True if ball lost (touched bottom wall)
        """
        ball_died = False
        _x, _y = map(int, self.get_position())
        _h, _w = map(int, self.get_shape())

        if _x == 0 or _x == config.WIDTH - 1 - _w:
            self.handle_collision(x_collision=True, y_collision=False)
        if _y == 0:
            self.handle_collision(x_collision=False, y_collision=True)
        if _y == config.HEIGHT - _h:
            # bottom wall touched
            self.destroy()
            ball_died = True

        return ball_died

    def handle_paddle_collision(self, paddle_middle):
        """Handle collision with paddle"""
        _x, _ = self.get_position()
        _x_vel, _ = self.get_velocity()
        self.handle_collision(x_collision=False, y_collision=True)
        self.set_xvelocity(_x_vel + int(_x - paddle_middle) * config.PADDLE_ACC)

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

    # def set_thru(self, thru: bool):
    #     """Make a ball thru or remove"""
    #     self._thru = thru
    #
    # def is_thru(self) -> bool:
    #     """Get if ball is thru"""
    #     return self._thru
