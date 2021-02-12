import numpy as np

import config


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
        return self._pos

    def get_shape(self):
        return self._rep.shape

    def get_rep(self):
        return self._rep, self._color


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
