import colorama
import numpy as np

import config
from .objects import GameObject, AutoMovingObject
from . import graphics


class UFO(GameObject):
    def __init__(self, pos):
        rep = GameObject.rep_from_str(graphics.UFO)
        color = np.array(["", colorama.Fore.CYAN + colorama.Style.BRIGHT])
        self._health = config.UFO_HEALTH
        super().__init__(rep, pos, color)

    def move_left(self):
        self.set_position(self.get_position() + np.array([-config.PADDLE_SPEED, 0]))

    def move_right(self):
        self.set_position(self.get_position() + np.array([config.PADDLE_SPEED, 0]))

    def get_health(self):
        return self._health

    def get_bomb_spawn_pos(self):
        x, y = self.get_position()
        h, w = self.get_shape()
        return np.array([x + w / 2, y + h])

    def handle_ball_collision(self):
        self._health -= 1
        if self._health <= 0:
            self.destroy()
            return True
        return False

    def get_health_bar(self):
        bar = ''
        for i in range(config.UFO_HEALTH):
            if i < self._health:
                bar += '#'
            else:
                bar += '_'
        return bar


class Bomb(AutoMovingObject):
    def __init__(self, pos):
        rep = GameObject.rep_from_str(graphics.BOMB)
        color = np.array(["", colorama.Fore.RED + colorama.Style.BRIGHT])
        vel = np.array([0, config.BOMB_SPEED])
        super().__init__(rep, pos, color, vel)
