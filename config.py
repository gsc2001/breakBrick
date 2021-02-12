import os
from colorama import Fore, Back, Style

# get the terminal screen size
scrh, scrw = map(int, os.popen('stty size', 'r').read().split())

WIDTH = scrw
HEIGHT = scrh - 10

FRAME_RATE = 20

# colors
BG_COLOR = Back.BLACK
FG_COLOR = Fore.GREEN

# paddle
PADDLE_WIDTH_NORMAL = 6
PADDLE_WIDTH_LONG = 8
PADDLE_WIDTH_SHORT = 4
PADDLE_SPEED = 1
