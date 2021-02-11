import signal

from .game import Game


def start_game():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    game = Game()
    game.start()


