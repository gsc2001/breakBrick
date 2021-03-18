import os

from colorama import Fore, Back, Style

# get the terminal screen size
scrh, scrw = map(int, os.popen('stty size', 'r').read().split())

DEBUG = True

BOSS_LEVEL = 3  # this is same as number of levels as the boss level is the last level

PADDLE_SPEED = 1

HEIGHT = scrh - 10
WIDTH = scrw

FRAME_RATE = 20

# colors
BG_COLOR = Back.BLACK
FG_COLOR = Fore.GREEN

# paddle
PADDLE_WIDTH_NORMAL = 17
PADDLE_WIDTH_MAX = 31
PADDLE_WIDTH_MIN = 15
PADDLE_CHANGE_AMT = 2

# ball
BALL_SPEED_NORMAL = 1
FAST_BALL_MULTIPLIER = 1.2

# collision buffer
COLLISION_BUFFER = 1

# brick
BRICK_START_HEIGHT = 0
BRICK_END_HEIGHT = 11
BRICK_MAP_DIR = 'levels'
BRICK_WIDTH = 6
BRICK_BREAK_SCORE = 100

# powerup
POWERUP_SPEED = 0.5
POWERUP_FRAMES = FRAME_RATE * 12
POWERUP_PROB = 0.1
