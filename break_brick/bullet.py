import colorama
import numpy as np

import config
from .objects import AutoMovingObject, GameObject
from .graphics import BULLET


class Bullet(AutoMovingObject):

    def __init__(self, pos):
        rep = GameObject.rep_from_str(BULLET)
        color = np.array(["", colorama.Fore.BLUE + colorama.Style.BRIGHT])
        vel = np.array([0, -config.BULLET_SPEED])
        super().__init__(rep, pos, color, vel)
