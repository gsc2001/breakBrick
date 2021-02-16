from colorama import Back, Fore
import numpy as np

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
