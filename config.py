import os
from colorama import Fore, Back, Style

# get the terminal screen size
scrh, scrw = map(int, os.popen('stty size', 'r').read().split())

WIDTH = scrw
HEIGHT = scrh - 10

FRAME_RATE = 30

# colors
BG_COLOR = Back.BLACK
FG_COLOR = Fore.GREEN

# paddle
PADDLE_WIDTH_NORMAL = 11
PADDLE_WIDTH_LONG = 15
PADDLE_WIDTH_SHORT = 9
PADDLE_SPEED = 1

# ball
Y_BALL_SPEED_NORMAL = 0.5

# collision buffer
COLLISION_BUFFER = 1

