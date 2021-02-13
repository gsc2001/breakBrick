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
        pos = np.array([config.WIDTH / 2, config.HEIGHT - 2])
        super().__init__(rep, pos, color, np.array([0, -config.Y_BALL_SPEED_NORMAL]))

    def _handle_collision(self, _from: utils.CollisionDirection):
        """
        Handle collision from the given direction
        :param _from: the direction from where the ball collided
        """
        if _from == utils.CollisionDirection.ABOVE:
            self._velocity[1] = -self._velocity[1]
            self.set_position(self._pos + np.array([0, 1]))
        elif _from == utils.CollisionDirection.BELLOW:
            self._velocity[1] = -self._velocity[1]
            self.set_position(self._pos + np.array([0, -1]))
        elif _from == utils.CollisionDirection.LEFT:
            self._velocity[0] = -self._velocity[0]
            self.set_position(self._pos + np.array([1, 0]))
        elif _from == utils.CollisionDirection.RIGHT:
            self._velocity[0] = -self._velocity[0]
            self.set_position(self._pos + np.array([-1, 0]))

    def handle_wall_collision(self) -> bool:
        """
        Handle ball collision with wall
        :return: True if ball lost (touched bottom wall)
        """
        ball_died = False
        _x, _y = self.get_position()

        if _x == 0:
            self._handle_collision(_from=utils.CollisionDirection.LEFT)
        if _x == config.WIDTH - 1:
            self._handle_collision(_from=utils.CollisionDirection.RIGHT)
        if _y == 0:
            self._handle_collision(_from=utils.CollisionDirection.ABOVE)
        if _y == config.HEIGHT - 1:
            # bottom wall touched
            self.destroy()
            ball_died = True

        return ball_died
