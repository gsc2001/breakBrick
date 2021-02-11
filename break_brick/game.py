import time
import sys

import colorama

from .screen import Screen
from .paddle import Paddle
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

        self._keyboard = utils.KBHit()
        self._screen = Screen()
        self._paddle = Paddle()
        utils.reset_screen()

    def _handle_input(self):
        """
        Handles input character if a key is pressed
        """
        if self._keyboard.kbhit():
            inp = self._keyboard.getch()

            if inp == 'q':
                sys.exit(0)
            elif inp == 'd':
                self._paddle.move_right()
            elif inp == 'a':
                self._paddle.move_left()

            self._keyboard.clear()
            
    def _draw_objects(self):
        self._screen.draw(self._paddle)

    def start(self):
        """
        Start the game
        """

        while True:
            start_time = time.perf_counter()
            self._screen.clear()
            self._handle_input()

            self._draw_objects()
            self._screen.show()

            while time.perf_counter() - start_time < 0.05:  # frame rate
                pass
