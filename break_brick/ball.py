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

    def __init__(self):
        rep = GameObject.rep_from_str(BALL)
        color = np.array([config.BG_COLOR, colorama.Fore.WHITE + colorama.Style.BRIGHT])
        pos = np.array([int(config.WIDTH / 2), config.HEIGHT - 4])
        super().__init__(rep, pos, color, np.array([config.Y_BALL_SPEED_NORMAL, config.Y_BALL_SPEED_NORMAL]))

    def handle_collision(self, _from: utils.CollisionDirection):
        """
        Handle collision from the given direction
        :param _from: the direction from where the ball collided
        """
        _vel = self.get_velocity()
        if _from == utils.CollisionDirection.X:
            self.set_xvelocity(-_vel[0])
            _vel[1] = 0
            self.set_position(self._pos + np.sign(-_vel))

        elif _from == utils.CollisionDirection.Y:
            self.set_yvelocity(-_vel[1])
            _vel[0] = 0
            self.set_position(self._pos + np.sign(-_vel))

    def handle_wall_collision(self) -> bool:
        """
        Handle ball collision with wall
        :return: True if ball lost (touched bottom wall)
        """
        ball_died = False
        _x, _y = map(int, self.get_position())
        _h, _w = map(int, self.get_shape())

        if _x == 0 or _x == config.WIDTH - 1 - _w:
            self.handle_collision(_from=utils.CollisionDirection.X)
        if _y == 0:
            self.handle_collision(_from=utils.CollisionDirection.Y)
        if _y == config.HEIGHT - _h:
            # bottom wall touched
            self.destroy()
            ball_died = True

        return ball_died
