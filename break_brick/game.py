from time import clock

import break_brick.utils as utils


class Game:
    """
    Class to handle whole game
    """

    def __init__(self):
        """
        Do some init calls
        """
        self.__keyboard = utils.KBHit()

    def _handle_input(self):
        """
        Handles input character if a key is pressed
        """
        if self.__keyboard.kbhit():
            inp = self.__keyboard.getch()


        self.__keyboard.clear()

    def start(self):
        """
        Start the game
        """

        while True:
            start_time = clock()

            self._handle_input()

            while clock() - start_time < 0.05:  # frame rate
                pass
