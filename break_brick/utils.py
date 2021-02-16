"""Some useful utillities"""
import atexit
from enum import Enum
from select import select
import sys
import termios


def reset_screen():
    """Positions the cursor on top left"""

    print("\033[0;0H")


def check_cross_dist(pa0, pa1, pb0, pb1, dist)->bool:
    """check if the min cross dist is < dist"""
    for _pa in [pa0, pa1]:
        for _pb in [pb0, pb1]:
            if abs(_pa - _pb) < 1:
                return True
    return False


class CollisionDirection(str, Enum):
    """Direction from where the collision has occured"""
    X = 'X'
    Y = 'Y'




class KBHit:
    """
    Class to get keyboard input
    modified version of "https://stackoverflow.com/a/22085679/13997197"
    """

    def __init__(self):
        """Create a object to play with keyboard"""

        # save old settings
        self.__fd = sys.stdin.fileno()
        self.__new_term = termios.tcgetattr(self.__fd)
        self.__old_term = termios.tcgetattr(self.__fd)

        # make the new terminal unbuffered
        self.__new_term[3] = (self.__new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.__fd, termios.TCSAFLUSH, self.__new_term)

        # restore normal-terminal setting on exit
        atexit.register(self.restore_terminal)

    def restore_terminal(self):
        """Reset the terminal to original state"""
        termios.tcsetattr(self.__fd, termios.TCSAFLUSH, self.__old_term)

    @staticmethod
    def kbhit():
        """Returns True if a keyboard character was hit, False otherwise"""
        return select([sys.stdin], [], [], 0)[0] != []

    @staticmethod
    def getch():
        """Returns the keyboard char after kbhit() has been called"""
        return sys.stdin.read(1)

    @staticmethod
    def clear():
        """Clear the input buffer"""
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
