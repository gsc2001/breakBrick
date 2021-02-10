import os
import numpy as np

import config

class Screen:

    """Class for screen of the game"""
    def __init__(self):
        """Init calls"""
        self.rows, self.cols = os.popen('stty size', 'r').read().split()

        self.__background = np.full((self.cols, self.rows), config.BG_COLOR)

        self.__foreground = np.full((self.cols, self.rows), ' ')



    def show(self):
        """Shows the screen"""




