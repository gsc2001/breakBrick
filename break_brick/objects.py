from typing import Tuple

import numpy as np

import config
import break_brick.utils as utils


# Bounding Box
# x0, y0 ----- x1, y0
# |                 |
# |                 |
# x0, y1 ----- x1, y1

class GameObject:
    """
    Basic game object
    has properties like pos, rep and active
    """

    def __init__(self, rep: np.ndarray, pos: np.ndarray = np.array([0., 0.]), color: np.ndarray = np.array(["", ""])):

        self._pos = pos
        self._active = True
        self._rep = rep
        self._color = GameObject.color_mask(rep, color)

    def destroy(self):
        """Destroy the object"""
        self._active = False

    @staticmethod
    def rep_from_str(rep_str: str) -> np.ndarray:
        """
        Get 2d array repr from string
        :param rep_str: representation string
        :return: 2d array of representation
        """

        _splits = rep_str.split('\n')[1:-1]
        _height = len(_splits)
        _width = max([len(a) for a in _splits])

        rep = np.full((_height, _width), " ")
        for i in range(_height):
            for j, ch in enumerate(_splits[i]):
                rep[i][j] = ch

        return rep

    @staticmethod
    def color_mask(rep: np.ndarray, color: np.ndarray = np.array(["", ""])) -> np.ndarray:
        """
        Get color mask
        :param rep: the representation
        :param color: color of the object
        :return: 3d array of color
        """
        _color = np.full((*rep.shape, 2), "", dtype=object)
        _color[:, :] = color
        _color[rep == " "] = [config.BG_COLOR, config.FG_COLOR]

        return _color

    def get_position(self):
        return self._pos.copy()

    def get_shape(self):
        return self._rep.shape

    def get_rep(self):
        return self._rep, self._color

    def set_position(self, new_pos: np.ndarray):
        """
        Set the position to new position
        :param new_pos: the new position
        """
        _h, _w = self.get_shape()
        self._pos = np.clip(new_pos, 0, [config.WIDTH - 1 - _w, config.WIDTH - 1 - _h])

    def is_active(self):
        return self._active

    def get_bounding_box(self):
        """Get bounding box of the object"""
        _h, _w = self.get_shape()
        _x, _y = self.get_position()

        return (_x, _x + _w), (_y, _y + _h)


class AutoMovingObject(GameObject):
    """
    Base class for all auto moving objects (i.e. except paddle)
    has properties like vel and other things
    """

    def __init__(self, rep: np.ndarray, pos: np.ndarray = np.array([0., 0.]), color: np.ndarray = np.array(["", ""]),
                 velocity: np.ndarray = np.array([0., 0.])):
        """
        Moving object constructor
        :param rep: the representation of object
        :param pos: initial position of object ([x,y])
        :param color: color of object ([bg, fg])
        :param velocity: initial velocity ([vx, vy])
        """
        super().__init__(rep, pos, color)
        self._velocity = velocity

    def update(self):
        """Update the position of a moving object"""
        # if not active just return
        if not self._active:
            return
        self.set_position(self._pos + self._velocity)

    def get_velocity(self):
        """
        Get velocity of the object
        :return: velocity as np.array([vx,vy])
        """
        return self._velocity.copy()

    def set_xvelocity(self, x_velocity):
        self._velocity[0] = x_velocity

    def set_yvelocity(self, y_velocity):
        self._velocity[1] = y_velocity


def detect_collision(obja: GameObject, objb: GameObject):
    """
    Detect collision between 2 objects
    :param obja: 1st object
    :param objb: 2nd object
    :return: tuple for x_collision , y_collision
    """

    (xa0, xa1), (ya0, ya1) = obja.get_bounding_box()
    (xb0, xb1), (yb0, yb1) = objb.get_bounding_box()

    # basic collision detection using rectangle intersection of with 1 expanded bounding box
    x_start = max(xb0, xa0)
    x_end = min(xa1, xb1)
    y_start = max(ya0 , yb0)
    y_end = min(ya1 , yb1)

    if x_start > x_end or y_start > y_end:
        # no collision
        return False, False

    x_collision = False
    y_collision = False

    if utils.check_cross_dist(xa0, xa1, xb0, xb1, config.COLLISION_BUFFER):
        x_collision = True

    if utils.check_cross_dist(ya0, ya1, yb0, yb1, config.COLLISION_BUFFER):
        y_collision = True

    return x_collision, y_collision
