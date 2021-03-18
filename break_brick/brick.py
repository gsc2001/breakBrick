from typing import List

from colorama import Back, Fore
import config
import numpy as np
import os

import break_brick.utils as utils
from .objects import GameObject
from .graphics import BRICK

colors = list(
    map(np.array, [[Back.GREEN, Fore.GREEN], [Back.YELLOW, Fore.YELLOW], [Back.RED, Fore.RED], [Back.BLUE, Fore.BLUE],
                   [Back.CYAN, Fore.CYAN]]))


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
        brick_width = len(BRICK) - 2
        bricks = []
        if not os.path.exists(path):
            raise SystemExit('Brick map not found')
        with open(path) as map_file:
            lines = map_file.readlines()
            for i, line in enumerate(lines):
                for j, _dig in enumerate(line.split(',')[:-1]):
                    if _dig == '4':
                        bricks.append(UnbreakableBrick(utils.get_arr(j * brick_width, config.BRICK_START_HEIGHT + i)))
                    elif _dig == '5':
                        bricks.append(ExplodingBrick(utils.get_arr(j * brick_width, config.BRICK_START_HEIGHT + i)))
                    elif _dig == '6':
                        bricks.append(RainbowBrick(utils.get_arr(j * brick_width, config.BRICK_START_HEIGHT + i)))
                    elif _dig != '0':
                        bricks.append(Brick(utils.get_arr(j * brick_width, config.BRICK_START_HEIGHT + i), int(_dig)))

        return bricks

    def _update_color(self):
        self.set_color(colors[self._health - 1])

    def hit(self, is_thru: bool, powerup_spawn, ball_vel) -> int:
        """
        Brick hit
        :return: Score addition
        """
        if is_thru:
            self._health = 0
        else:
            self._health -= 1
        if self._health == 0:
            self.destroy()
            powerup_spawn(self.get_position(), ball_vel)
            return config.BRICK_BREAK_SCORE
        self._update_color()
        return 0

    def handle_ball_collision(self, is_thru: bool, powerup_spawn, ball_vel) -> int:
        """
        Handle brick <-> ball collision w.r.t brick
        :param ball_vel: velocity of the ball
        :param powerup_spawn: function to spawn power up if brick breaks
        :param is_thru: is ball a thru one
        :return: Score addition
        """
        return self.hit(is_thru, powerup_spawn, ball_vel)


class UnbreakableBrick(Brick):
    """Class for a unbreakable brick"""

    def __init__(self, pos):
        # temp health to set color
        health = 4
        super().__init__(pos, health)
        self._health = np.inf

    def hit(self, is_thru: bool, powerup_spawn, ball_vel):
        """No need to do anything to the brick"""
        if is_thru:
            self.destroy()
            powerup_spawn(self.get_position(), ball_vel)
            return config.BRICK_BREAK_SCORE
        return 0


class ExplodingBrick(Brick):
    """Class for an exploding brick"""

    def __init__(self, pos):
        health = 1
        super().__init__(pos, health)
        self.set_color(colors[4])

    def hit(self, bricks: List[Brick], powerup_spawn, ball_vel) -> int:
        """Exploding brick hit"""

        # Run a dfs to hit bricks in surrounding 8 directions
        self.destroy()
        _pos = self.get_position()
        _h, _w = self.get_shape()
        affected_pos = [_pos + np.array([-_w, 0]),
                        _pos + np.array([_w, 0]),
                        _pos + np.array([_w, _h]),
                        _pos + np.array([_w, -_h]),
                        _pos + np.array([-_w, _h]),
                        _pos + np.array([-_w, -_h]),
                        _pos + np.array([0, _h]),
                        _pos + np.array([0, -_h])]
        score = 0
        for _brick in bricks:
            if not _brick.is_active():
                continue
            _brick_pos = _brick.get_position()
            if _brick_pos.tolist() in list(map(list, affected_pos)):
                if isinstance(_brick, ExplodingBrick):
                    score += _brick.hit(bricks, powerup_spawn, ball_vel)
                else:
                    score += _brick.hit(True, powerup_spawn, ball_vel)
        powerup_spawn(self.get_position(), ball_vel)
        return score


class RainbowBrick(Brick):
    def __init__(self, pos):
        health = 3
        self._changing = True
        super().__init__(pos, health)

    def update(self):
        if not self._changing:
            return
        self._health += 1
        if self._health == 4:
            self._health = 1

        self._update_color()

    def hit(self, *args) -> int:
        self._changing = False
        return super().hit(*args)
