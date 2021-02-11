import os
import sys

import colorama
import numpy as np

import config
import break_brick.utils as utils


class Screen:
    """Class for screen of the game"""

    def __init__(self):
        """Init calls"""
        self.__scrh, self.__scrr = map(int, os.popen('stty size', 'r').read().split())
        self.rows = self.__scrh - 10
        self.cols = self.__scrr

        self.display = np.full((self.rows, self.cols), " ")
        self.color = np.full((self.rows, self.cols, 2), "", dtype=object)
        self.clear()

    def clear(self):
        """Clears the whole display"""
        utils.reset_screen()
        self.display[:] = " "
        self.color[:, :, 0] = config.BG_COLOR  # set the BG color
        self.color[:, :, 1] = config.FG_COLOR  # set the FG color

    def draw(self, pos: tuple, char: str):
        """Puts a character at pos"""
        self.display[pos] = char
        self.color[pos] = [colorama.Back.WHITE, colorama.Fore.BLUE]

    def show(self):
        """Shows the screen"""
        out = ""

        for i in range(self.rows):
            for j in range(self.cols):
                out += "".join(self.color[i][j]) + self.display[i][j]
            out += '\n'

        sys.stdout.write(out + colorama.Style.RESET_ALL)
