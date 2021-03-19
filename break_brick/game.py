import time
import sys

import colorama
import numpy as np
import os

import config
from .screen import Screen
from .paddle import Paddle
from .ball import Ball
from .bullet import Bullet
from .brick import Brick, ExplodingBrick, UnbreakableBrick, RainbowBrick
from .objects import detect_collision
from .ufo import UFO, Bomb
from .powerup import ExpandPaddle, ShrinkPaddle, FastBall, BallMultiplier, ThruBall, PaddleGrab, ShootingPaddle
import break_brick.utils as utils

powerup_options = [ExpandPaddle, ShrinkPaddle, FastBall, BallMultiplier, ThruBall, PaddleGrab, ShootingPaddle]


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
        self._bomb_timer = config.BOMB_TIMER
        self._level_end_time = time.time() + config.FALLING_BRICK_TIME
        self._start_time = time.time()

        # For debug
        # self._balls = [Ball(np.array([1, config.HEIGHT - 19]), np.array([config.BALL_SPEED_NORMAL, 0]))]
        self._balls = []
        self._reset_ball()
        # self._bricks = [Brick(np.array([config.WIDTH // 2 - 2, config.HEIGHT - 17]), 3)]
        self._bricks = []
        # TODO: Add a key to skip levels
        self._power_ups = []
        self._bullets = []
        self._bombs = []
        self._ufo = None
        self._load_level(1)
        self._thru_balls = False  # variable to signify if the ball are thru or not
        self._falling_bricks = False  # To signify if the falling bricks is going on
        self._shooting_paddle = False
        self._next_shoot = 0
        self._won = False
        utils.reset_screen()

    def _is_boss_level(self):
        return self._current_level == config.BOSS_LEVEL

    def _create_boss_level(self):
        self._bricks = []
        _x, _ = self._paddle.get_position()
        self._ufo = UFO(utils.get_arr(_x, 3))

    def _reset_ball(self):
        _paddle_pos = self._paddle.get_position()
        _paddle_middle, _ = self._paddle.get_middle()
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
            # GAME WON
            self._game_over(True)
            return

        self._load_level(self._current_level + 1)

    def _load_level(self, level: int):
        if config.DEBUG:
            assert 1 <= level <= config.BOSS_LEVEL

        self._current_level = level
        self._level_end_time = time.time() + config.FALLING_BRICK_TIME

        if self._is_boss_level():
            self._create_boss_level()

        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config.BRICK_MAP_DIR,
                                 f'level_{self._current_level}.txt')
        self._bricks = Brick.get_brick_map(file_path)

        # Remove all powerups
        with open('logs', 'w') as f:
            f.write(f'{self._current_level}\n')
            for powerup in self._power_ups:
                f.write(f'{powerup.is_activated()}, {powerup.is_active()}, {powerup}, {id(powerup)}\n')

        for powerup in self._power_ups:
            if not powerup.is_active():
                continue
            if powerup.is_falling():
                powerup.destroy()
            else:
                self._deactivate_powerup(powerup)

        for bullet in self._bullets:
            bullet.destroy()

        self._power_ups = []
        self._bullets = []
        self._falling_bricks = False
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
                if self._is_boss_level():
                    self._ufo.move_right()
            elif inp == 'a':
                self._paddle.move_left()
                if self._is_boss_level():
                    self._ufo.move_left()
            elif inp == 'n':
                self._increase_level()
            elif inp == ' ':
                self._paddle.remove_ball()

            self._keyboard.clear()

    def drop_bomb(self):
        assert self._ufo is not None
        self._bombs.append(Bomb(self._ufo.get_bomb_spawn_pos()))

    def _try_drop_bomb(self):
        if not self._is_boss_level():
            return

        self._bomb_timer -= 1
        if self._bomb_timer <= 0:
            self.drop_bomb()
            self._bomb_timer = config.BOMB_TIMER

    def _ufo_defense(self):
        assert self._ufo is not None
        _, y = self._ufo.get_bomb_spawn_pos()

        n_bricks = config.WIDTH // config.BRICK_WIDTH
        brick_x = np.array(range(n_bricks)) * config.BRICK_WIDTH

        affected_positions = np.ndarray((len(brick_x), 2))
        affected_positions[:, 0] = brick_x
        affected_positions[:, 1] = y

        empty = np.ones_like(brick_x)

        breakable = list(filter(lambda b: not isinstance(b, UnbreakableBrick), self._bricks))
        for brick in breakable:
            empty[(brick.get_position() == affected_positions)[:, 0]] = 0

        for i, pos in enumerate(affected_positions):
            if empty[i]:
                self._bricks.append(Brick(np.array(pos), np.random.randint(low=1, high=4)))

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
        else:
            # powerups which can be applied only once, just extend the time of the prev one
            f = open('logs2', 'a')
            f.write('\n\n---\n')
            f.write(f'level: {self._current_level}\n')
            f.write(f'powerups: {self._power_ups}\n')
            f.write((f'powerup: {powerup.is_active()}'))

            existing = list(
                filter(lambda _powerup: isinstance(_powerup, type(powerup)) and _powerup.is_activated(),
                       self._power_ups))
            f.write(f'existing: {existing}\n')
            if len(existing) != 0:
                if config.DEBUG:
                    assert len(existing) == 1
                existing[0].add_time(config.POWERUP_FRAMES)
                powerup.destroy()
                return
            if isinstance(powerup, ThruBall):
                self._thru_balls = powerup.activate()
            elif isinstance(powerup, PaddleGrab):
                powerup.activate(self._paddle)
            elif isinstance(powerup, ShootingPaddle):
                self._shooting_paddle = powerup.activate(self._paddle)

            existing = list(
                filter(lambda _powerup: isinstance(_powerup, type(powerup)) and _powerup.is_activated(),
                       self._power_ups))
            f.write(f'new existing: {existing[0].is_activated()}\n')
            f.close()

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
        elif isinstance(powerup, ShootingPaddle):
            self._shooting_paddle = powerup.deactivate(self._paddle)

    def try_spawn_powerup(self, pos, vel):
        if self._is_boss_level():
            return
        # do_spawn = np.random.random() > 1 - config.POWERUP_PROB
        do_spawn = True
        if do_spawn:
            # self._power_ups.append(powerup_options[np.random.randint(0, 7)](pos, vel))
            self._power_ups.append(ShootingPaddle(pos, vel))

    def _update_objects(self):
        for ball in self._balls:
            ball.update()

        rainbow_bricks = filter(lambda _brick: isinstance(_brick, RainbowBrick), self._bricks)
        for brick in rainbow_bricks:
            brick.update()
        for bullet in self._bullets:
            bullet.update()

        for bomb in self._bombs:
            bomb.update()

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

        for bullet in self._bullets:
            if bullet.is_active():
                self._screen.draw(bullet)

        if self._is_boss_level():
            if config.DEBUG:
                assert self._ufo is not None
            print(self._ufo)
            self._screen.draw(self._ufo)
            for bomb in self._bombs:
                if bomb.is_active():
                    self._screen.draw(bomb)

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

        for i, _bullet in enumerate(self._bullets):
            if not _bullet.is_active():
                self._bullets.pop(i)

        for i, _bomb in enumerate(self._bombs):
            if not _bomb.is_active():
                self._bombs.pop(i)

    def _game_over(self, won: bool):
        self._playing = False
        self._won = won

    def _check_live_end(self):
        if len(list(filter(lambda ball: ball.is_active(), self._balls))) == 0:
            self._lives -= 1
            self._reset_ball()
            if self._lives == 0:
                # GAME LOST
                self._game_over(False)

    def _check_level_change(self):
        breakable_bricks = list(filter(lambda brick: not isinstance(brick, UnbreakableBrick), self._bricks))
        if len(breakable_bricks) == 0 and not self._is_boss_level():
            self._increase_level()
        if self._is_boss_level():
            if not self._ufo.is_active():
                # GAME WON
                self._game_over(True)

    def _check_falling_start(self):
        if time.time() >= self._level_end_time:
            self._falling_bricks = True

    def _fall_bricks(self):
        _, paddle_y = self._paddle.get_position()

        for brick in self._bricks:
            if not brick.is_active():
                continue
            x, y = brick.get_position()
            h, _ = brick.get_shape()
            if paddle_y - (y + 1 + h) == 0:
                # GAME OVER
                self._game_over(False)
                return
            brick.set_position(np.array([x, y + 1]))

    def _handle_collisions(self):
        """Handle collision of objects"""

        for i, ball in enumerate(self._balls):
            # check collision with wall
            ball.handle_wall_collision()

            # check collision with paddle
            _x_col, _y_col = detect_collision(ball, self._paddle)
            if _y_col or _x_col:
                ball.handle_paddle_collision(self._paddle.get_middle()[0], self._paddle.get_shape()[1])
                if self._falling_bricks:
                    self._fall_bricks()
                if self._paddle.is_sticky():
                    self._paddle.stick_ball(ball)

            # check collision with bricks
            for _, brick in enumerate(self._bricks):
                _x_col, _y_col = detect_collision(ball, brick)
                if _x_col or _y_col:
                    ball_vel = ball.get_velocity()
                    ball.handle_brick_collision(_x_col, _y_col, self._thru_balls)
                    _tscore = 0
                    if isinstance(brick, ExplodingBrick):
                        self._score += brick.handle_ball_collision(self._bricks, self.try_spawn_powerup, ball_vel)
                    else:
                        self._score += brick.handle_ball_collision(self._thru_balls, self.try_spawn_powerup, ball_vel)

            # check collision with ufo
            if self._is_boss_level():
                _x_col, _y_col = detect_collision(ball, self._ufo)
                if _x_col or _y_col:
                    ball.handle_brick_collision(_x_col, _y_col, self._thru_balls)
                    self._ufo.handle_ball_collision()
                    if self._ufo.get_health() == 0.5 * config.UFO_HEALTH:
                        self._ufo_defense()
                    elif self._ufo.get_health() == 0.2 * config.UFO_HEALTH:
                        self._ufo_defense()

        for i, powerup in enumerate(self._power_ups):
            # check if the powerup has touched the ground
            if powerup.is_activated():
                continue
            powerup.handle_wall_collision()
            _x_col, _y_col = detect_collision(self._paddle, powerup)
            if _x_col or _y_col:
                self._activate_powerup(powerup)

        for bullet in self._bullets:
            bullet.handle_wall_collision(kill=True)
            for brick in self._bricks:
                _x_col, _y_col = detect_collision(bullet, brick)
                if _x_col or _y_col:
                    bullet_vel = bullet.get_velocity()
                    bullet.destroy()
                    if isinstance(brick, ExplodingBrick):
                        self._score += brick.handle_ball_collision(self._bricks, self.try_spawn_powerup, bullet_vel)
                    else:
                        self._score += brick.handle_ball_collision(self._thru_balls, self.try_spawn_powerup, bullet_vel)
        if self._is_boss_level():
            for bomb in self._bombs:
                bomb.handle_wall_collision(kill=True)
                _x_col, _y_col = detect_collision(bomb, self._paddle)
                if _x_col or _y_col:
                    # loose a life
                    bomb.destroy()
                    self._lives -= 1
                    if self._lives == 0:
                        self._game_over(False)

    def _shoot_if_possible(self):
        if not self._shooting_paddle:
            return
        self._next_shoot -= 1
        if self._next_shoot <= 0:
            middle = self._paddle.get_middle()
            self._bullets.append(Bullet(middle + np.array([0, -1])))
            self._next_shoot = config.BULLET_DELAY_FRAMES

    def print_game_info(self):
        current_time = time.time()
        print(colorama.Style.RESET_ALL + colorama.Fore.WHITE + colorama.Style.BRIGHT + colorama.Back.BLACK)
        print(f"Level: {self._current_level}")
        print(f"Lives: {self._lives}")
        print(f"Score: {self._score}")
        print(f"Time: {int(current_time - self._start_time)}")
        time_attack = max(0.0, round(self._level_end_time - current_time, 2))
        if not self._falling_bricks:
            print(f"Time attack in {time_attack}")
        else:
            print("Time attack going on!")
        if self._shooting_paddle:
            powerup = list(filter(
                lambda _pow: isinstance(_pow, ShootingPaddle) and _pow.is_activated(), self._power_ups))[0]
            print(f'Shooting paddle time left: {round(powerup.get_time() / config.FRAME_RATE, 2)}')
        if self._is_boss_level():
            print("UFO: " + self._ufo.get_health_bar())
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
            self._shoot_if_possible()
            self._try_drop_bomb()
            self._handle_collisions()
            self._update_objects()
            self._clean()
            self._check_live_end()
            self._check_level_change()
            self._check_falling_start()
            self.print_game_info()
            self._draw_objects()
            self._screen.show()

            while time.perf_counter() - start_time < 1 / config.FRAME_RATE:  # frame rate
                pass

        utils.reset_screen()
        print(colorama.Style.BRIGHT + colorama.Fore.WHITE)
        if self._won:
            print("YOU WON!!")
        else:
            print("YOU LOST :(")
        print(colorama.Style.RESET_ALL)
