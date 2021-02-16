import os
from colorama import Fore, Back, Style

# get the terminal screen size
scrh, scrw = map(int, os.popen('stty size', 'r').read().split())

PADDLE_SPEED = 3

HEIGHT = scrh - 10
WIDTH = min(scrw, HEIGHT*PADDLE_SPEED)

FRAME_RATE = 30

# colors
BG_COLOR = Back.BLACK
FG_COLOR = Fore.GREEN

# paddle
PADDLE_WIDTH_NORMAL = 11
PADDLE_WIDTH_LONG = 15
PADDLE_WIDTH_SHORT = 9
PADDLE_ACC = 0.2

# ball
BALL_SPEED_NORMAL = 0.5

# collision buffer
COLLISION_BUFFER = 1

