import sys

import colorama
import numpy as np

import config
import break_brick.utils as utils
from .objects import GameObject


# + ---> x
# |
# |
# v
# y

class Screen:
    """Class for screen of the game"""

    def __init__(self):
        """Init calls"""
        self.height = config.HEIGHT
        self.width = config.WIDTH

        self.display = np.full((self.height, self.width), ".")
        self.color = np.full((self.height, self.width, 2), "", dtype=object)
        self.clear()

    def clear(self):
        """Clears the whole display"""
        utils.reset_screen()
        self.display[:] = "."
        self.color[:, :, 0] = config.BG_COLOR  # set the BG color
        self.color[:, :, 1] = config.FG_COLOR  # set the FG color

    def draw(self, obj: GameObject):
        """
        Puts an object on screen
        :param obj: the obj to put
        """
        _x, _y = map(int, obj.get_position())
        _rep, _color = obj.get_rep()
        _h, _w = map(int, _rep.shape)

        self.display[_y: _y + _h, _x:_x + _w] = _rep
        self.color[_y: _y + _h, _x:_x + _w] = _color

    def show(self):
        """Shows the screen"""
        out = ""

        for i in range(self.height):
            for j in range(self.width):
                out += "".join(self.color[i][j]) + self.display[i][j] + colorama.Style.RESET_ALL
            out += '\n'

        sys.stdout.write(out + colorama.Style.RESET_ALL)
