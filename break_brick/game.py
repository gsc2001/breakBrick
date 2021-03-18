import time
import sys

import colorama
import numpy as np
import os

import config
from .screen import Screen
from .paddle import Paddle
from .ball import Ball
from .brick import Brick, ExplodingBrick, UnbreakableBrick
from .objects import detect_collision
from .powerup import ExpandPaddle, ShrinkPaddle, FastBall, BallMultiplier, ThruBall, PaddleGrab
import break_brick.utils as utils

powerup_options = [ExpandPaddle, ShrinkPaddle, FastBall, BallMultiplier, ThruBall, PaddleGrab]


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
        self._lives = 3
        self._score = 0
        self._current_level = 1
        self._start_time = time.time()

        # For debug
        # self._balls = [Ball(np.array([1, config.HEIGHT - 19]), np.array([config.BALL_SPEED_NORMAL, 0]))]
        self._balls = []
        self._reset_ball()
        # self._bricks = [Brick(np.array([config.WIDTH // 2 - 2, config.HEIGHT - 17]), 3)]
        self._bricks = []
        # TODO: Add a key to skip levels
        self._power_ups = []
        self._load_level(1)
        self._thru_balls = False  # variable to signify if the ball are thru or not
        utils.reset_screen()

    def _reset_ball(self):
        _paddle_pos = self._paddle.get_position()
        _paddle_middle = self._paddle.get_middle()
        _, _w = self._paddle.get_shape()
        if config.DEBUG:
            _x_pos = int(_paddle_pos[0] + _w / 2)
        else:
            _x_pos = np.random.randint(_paddle_pos[0], _paddle_pos[0] + _w)

        _x_vel = int(_x_pos - _paddle_middle) / _w

        _vel = np.array([_x_vel, -config.BALL_SPEED_NORMAL])

        ball = Ball(pos=np.array([_x_pos, _paddle_pos[1] - 2]), vel=_vel)

        self._balls = [ball]
        self._paddle.stick_ball(self._balls[0])

    def _increase_level(self):
        if self._current_level == config.BOSS_LEVEL:
            # GAME Finished
            self._playing = False
            return

        self._load_level(self._current_level + 1)

    def _load_level(self, level: int):
        self._current_level = level
        if config.DEBUG:
            assert 1 <= self._current_level <= config.BOSS_LEVEL

        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config.BRICK_MAP_DIR,
                                 f'level_{self._current_level}.txt')
        self._bricks = Brick.get_brick_map(file_path)

        # Remove all powerups
        for powerup in self._power_ups:
            if not powerup.is_active():
                continue
            if not powerup.is_activated():
                powerup.destroy()
            else:
                self._deactivate_powerup(powerup)
        self._reset_ball()

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
            elif inp == ' ':
                self._paddle.remove_ball()

            self._keyboard.clear()

    def _activate_powerup(self, powerup):
        if config.DEBUG:
            assert not powerup.is_activated(), f'[ERROR] Powerup activating again type: {type(powerup)}'
        if isinstance(powerup, (ExpandPaddle, ShrinkPaddle)):
            powerup.activate(self._paddle)
        elif isinstance(powerup, FastBall):
            powerup.activate(self._balls)
        elif isinstance(powerup, BallMultiplier):
            new_balls = powerup.activate(self._balls)
            self._balls.extend(new_balls)
        elif isinstance(powerup, ThruBall):
            self._thru_balls = powerup.activate()
        elif isinstance(powerup, PaddleGrab):
            powerup.activate(self._paddle)

    def _deactivate_powerup(self, powerup):
        if config.DEBUG:
            assert powerup.is_activated(), f"[ERROR] Powerup deactivate without activate type: {type(powerup)}"
        if isinstance(powerup, (ExpandPaddle, ShrinkPaddle)):
            powerup.deactivate(self._paddle)
        elif isinstance(powerup, FastBall):
            powerup.deactivate(self._balls)
        elif isinstance(powerup, ThruBall):
            self._thru_balls = powerup.deactivate()
        elif isinstance(powerup, PaddleGrab):
            powerup.deactivate(self._paddle)

    def try_spawn_powerup(self, pos):
        do_spawn = np.random.random() > 1 - config.POWERUP_PROB

        if do_spawn:
            self._power_ups.append(powerup_options[np.random.randint(0, 6)](pos))

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

        for i, _power_up in enumerate(self._power_ups):
            if not _power_up.is_active():
                self._power_ups.pop(i)

        for i, _brick in enumerate(self._bricks):
            if not _brick.is_active():
                self._bricks.pop(i)

    def _check_live_end(self):
        if len(list(filter(lambda ball: ball.is_active(), self._balls))) == 0:
            self._lives -= 1
            self._reset_ball()
            if self._lives == 0:
                self._playing = False

    def _check_level_change(self):
        breakable_bricks = list(filter(lambda brick: not isinstance(brick, UnbreakableBrick), self._bricks))
        if len(breakable_bricks) == 0:
            self._increase_level()

    def _handle_collisions(self):
        """Handle collision of objects"""

        for i, ball in enumerate(self._balls):
            # check collision with wall
            ball.handle_wall_collision()

            # check collision with paddle
            _x_col, _y_col = detect_collision(ball, self._paddle)
            if _y_col or _x_col:
                ball.handle_paddle_collision(self._paddle.get_middle(), self._paddle.get_shape()[1])
                if self._paddle.is_sticky():
                    self._paddle.stick_ball(ball)

            # check collision with bricks
            for _, brick in enumerate(self._bricks):
                _x_col, _y_col = detect_collision(ball, brick)
                if _x_col or _y_col:
                    ball.handle_brick_collision(_x_col, _y_col, self._thru_balls)
                    _tscore = 0
                    if isinstance(brick, ExplodingBrick):
                        self._score += brick.handle_ball_collision(self._bricks, self.try_spawn_powerup)
                    else:
                        self._score += brick.handle_ball_collision(self._thru_balls, self.try_spawn_powerup)

        for i, powerup in enumerate(self._power_ups):
            # check if the powerup has touched the ground
            if powerup.is_activated():
                continue
            powerup.handle_wall_collision()
            _x_col, _y_col = detect_collision(self._paddle, powerup)
            if _x_col or _y_col:
                self._activate_powerup(powerup)

    def print_game_info(self):
        print(colorama.Style.RESET_ALL + colorama.Fore.WHITE + colorama.Style.BRIGHT + colorama.Back.BLACK)
        print(f"Lives: {self._lives}")
        print(f"Score: {self._score}")
        print(f"Time: {int(time.time() - self._start_time)}")
        print(colorama.Style.RESET_ALL, end='')

    def debug_info(self):
        """Print useful debug info"""
        print('------------------')
        print("Paddle: ", self._paddle._rep.shape)
        print("Balls: ")
        for ball in self._balls:
            print(ball._stored_velocity)
        print("Powerups")
        for _powerup in self._power_ups:
            print(_powerup, '\n')
        print('-------------------')

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
            self._check_live_end()
            self._check_level_change()
            self.print_game_info()
            self._draw_objects()
            self._screen.show()

            while time.perf_counter() - start_time < 1 / config.FRAME_RATE:  # frame rate
                pass
