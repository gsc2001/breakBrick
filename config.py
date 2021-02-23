import os

from colorama import Fore, Back, Style


# get the terminal screen size
scrh, scrw = map(int, os.popen('stty size', 'r').read().split())

PADDLE_SPEED = 3

HEIGHT = scrh - 10
WIDTH = scrw

FRAME_RATE = 39

# colors
BG_COLOR = Back.BLACK
FG_COLOR = Fore.GREEN

# paddle
PADDLE_WIDTH_NORMAL = 11
PADDLE_WIDTH_LONG = 15
PADDLE_WIDTH_SHORT = 9
PADDLE_ACC = 0.2

# ball
BALL_SPEED_NORMAL = 0.2
FAST_BALL_MULTIPLIER=1.1

# collision buffer
COLLISION_BUFFER = 1

# brick
BRICK_START_HEIGHT = 0
BRICK_END_HEIGHT = 7
BRICK_MAP_FILE = 'brickmap.txt'
BRICK_WIDTH = 6


# powerup
POWERUP_SPEED = 0.3
POWERUP_FRAMES = FRAME_RATE * 5


