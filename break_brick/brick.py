from colorama import Back, Fore
import config
import numpy as np
import os

import break_brick.utils as utils
from .objects import GameObject
from .graphics import BRICK

colors = list(map(np.array, [[Back.GREEN, Fore.GREEN], [Back.YELLOW, Fore.YELLOW], [Back.RED, Fore.RED]]))


class Brick(GameObject):
    """Class for a brick"""

    def __init__(self, pos, health):
        """Create a brick at pos `pos` and health `health`"""
        rep = GameObject.rep_from_str(BRICK)
        self._health = health
        super().__init__(rep, pos, colors[self._health - 1])

    @staticmethod
    def get_brick_map(path: str):
        """
        Get brick map
        :param path: the file path to txt file
        :return: list of bricks
        """
        bricks = []
        if not os.path.exists(path):
            raise SystemExit('Brick map not found')
        with open(path) as map_file:
            lines = map_file.readlines()
            if len(lines) != config.BRICK_END_HEIGHT - config.BRICK_START_HEIGHT + 1:
                raise SystemExit('Invalid brick map. height not matching')

            for i, line in enumerate(lines):
                for j, _dig in enumerate(line.split(',')[:-1]):
                    if _dig != '0':
                        bricks.append(Brick(utils.get_arr(j * 6, config.BRICK_START_HEIGHT + i), int(_dig)))

        return bricks

    def _update_color(self):
        self.set_color(colors[self._health - 1])

    def hit(self) -> bool:
        """
        Brick hit
        :return: Brick died or not
        """
        self._health -= 1
        if self._health == 0:
            self.destroy()
            return True
        self._update_color()
        return False

    def handle_ball_collision(self) -> bool:
        """
        Handle collision with ball
        :return: Brick died or not
        """
        return self.hit()
