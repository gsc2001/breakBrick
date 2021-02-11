import time
import sys

import colorama

from .screen import Screen
import break_brick.utils as utils


class Game:
    """
    Class to handle whole game
    """

    def __init__(self):
        """
        Do some init calls
        """
        colorama.init()
        # clear the screen
        print("\033[?25l\033[2J", end='')

        self.__keyboard = utils.KBHit()
        self.__screen = Screen()
        utils.reset_screen()

    def _handle_input(self):
        """
        Handles input character if a key is pressed
        """
        if self.__keyboard.kbhit():
            inp = self.__keyboard.getch()

            if inp == 'q':
                sys.exit(0)

            self.__screen.draw((10, 10), inp)

        self.__keyboard.clear()

    def start(self):
        """
        Start the game
        """

        while True:
            start_time = time.perf_counter()
            self.__screen.clear()

            self._handle_input()
            self.__screen.show()

            while time.perf_counter() - start_time < 0.05:  # frame rate
                pass
