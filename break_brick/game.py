import time
import sys

import colorama
import numpy as np
import os

import config
from .screen import Screen
from .paddle import Paddle
from .ball import Ball
from .brick import Brick
from .objects import detect_collision
from .powerup import ExpandPaddle
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
        self._playing = True
        self._keyboard = utils.KBHit()
        self._screen = Screen()
        self._paddle = Paddle()

        # For debug
        # self._balls = [Ball(np.array([1, config.HEIGHT - 19]), np.array([config.BALL_SPEED_NORMAL, 0]))]
        # self._balls = []
        self._balls = [Ball()]
        # self._bricks = [Brick(np.array([config.WIDTH // 2 - 2, config.HEIGHT - 17]), 3)]
        brick_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config.BRICK_MAP_FILE)
        self._bricks = Brick.get_brick_map(brick_file_path)
        self._power_ups = [ExpandPaddle(self._bricks[0].get_position())]
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

    def _activate_powerup(self, powerup):
        if isinstance(powerup, ExpandPaddle):
            powerup.activate(self._paddle)
        # more powerups here

    def _deactivate_powerup(self, powerup):
        if isinstance(powerup, ExpandPaddle):
            powerup.deactivate(self._paddle)
        # more powerups here

    def _update_objects(self):
        for ball in self._balls:
            ball.update()
        for powerup in self._power_ups:
            if powerup.is_falling():
                powerup.update()
            else:
                if powerup.reduce_time():
                    # powerup finished
                    self._deactivate_powerup(powerup)

    def _draw_objects(self):

        self._screen.draw(self._paddle)

        for brick in self._bricks:
            if brick.is_active():
                self._screen.draw(brick)

        for ball in self._balls:
            if ball.is_active():
                self._screen.draw(ball)

        for powerup in self._power_ups:
            if powerup.is_falling():
                self._screen.draw(powerup)

    def _clean(self):
        """Remove objects which are not active"""
        for i, _ball in enumerate(self._balls):
            if not _ball.is_active():
                self._balls.pop(i)
                self._check_game_over()

        for i, _power_up in enumerate(self._power_ups):
            if not _power_up.is_active():
                self._power_ups.pop(i)

        for i, _brick in enumerate(self._bricks):
            if not _brick.is_active():
                self._bricks.pop(i)

    def _check_game_over(self):
        if len(list(filter(lambda ball: ball.is_active(), self._balls))) == 0:
            self._playing = False

    def _handle_collisions(self):
        """Handle collision of objects"""

        for i, ball in enumerate(self._balls):
            # check collision with wall
            ball.handle_wall_collision()

            # check collision with paddle
            _x_col, _y_col = detect_collision(ball, self._paddle)
            if _y_col:
                ball.handle_paddle_collision(self._paddle.get_middle())

            # check collision with bricks
            for i, brick in enumerate(self._bricks):
                _x_col, _y_col = detect_collision(ball, brick)
                if _x_col or _y_col:
                    ball.handle_brick_collision(_x_col, _y_col)
                    brick.handle_ball_collision()

        for i, powerup in enumerate(self._power_ups):
            # check if the powerup has touched the ground
            powerup.handle_wall_collision()
            _x_col, _y_col = detect_collision(self._paddle, powerup)
            if _x_col or _y_col:
                self._activate_powerup(powerup)

    def start(self):
        """
        Start the game
        """

        while self._playing:
            start_time = time.perf_counter()
            self._screen.clear()
            self._handle_input()
            self._handle_collisions()
            self._update_objects()
            self._clean()
            self._draw_objects()
            self._screen.show()
            print("Paddle:", self._paddle._rep.shape)

            while time.perf_counter() - start_time < 1 / config.FRAME_RATE:  # frame rate
                pass
