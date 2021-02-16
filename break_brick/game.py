import time
import sys

import colorama
import numpy as np

import config
from .screen import Screen
from .paddle import Paddle
from .ball import Ball
from .brick import Brick
from .objects import detect_collision
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

        self._balls = [Ball()]
        self._bricks = [Brick(np.array([config.WIDTH // 2 - 2, config.HEIGHT - 20]), 3)]
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


    def _update_objects(self):
        for ball in self._balls:
            ball.update()

    def _draw_objects(self):

        self._screen.draw(self._paddle)

        for brick in self._bricks:
            if brick.is_active():
                self._screen.draw(brick)

        for ball in self._balls:
            if ball.is_active():
                self._screen.draw(ball)

    def _check_game_over(self):
        if len(list(filter(lambda ball: ball.is_active(), self._balls))) == 0:
            self._playing = False

    def _handle_collisions(self):
        """Handle collision of objects"""

        for i, ball in enumerate(self._balls):
            # check collision with wall
            if ball.handle_wall_collision():
                # bottom wall touched
                self._balls.pop(i)
                self._check_game_over()

            # check collision with paddle
            _x_col, _y_col = detect_collision(ball, self._paddle)
            if _y_col:
                ball.handle_paddle_collision(self._paddle.get_middle())

            # check collision with bricks
            for i, brick in enumerate(self._bricks):
                _x_col, _y_col = detect_collision(ball, brick)
                if _x_col or _y_col:
                    ball.handle_brick_collision(_x_col, _y_col)
                    if brick.handle_ball_collision():
                        self._bricks.pop(i)





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
            self._draw_objects()
            self._screen.show()

            while time.perf_counter() - start_time < 1 / config.FRAME_RATE:  # frame rate
                pass
