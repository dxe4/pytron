import curses
import time
from random import randint
import math

SIZE = 100

board = [i for i in range(0, SIZE) for j in range(0, SIZE)]

class Board(object):
    def __init__(self, players_size=4):
        if players_size not in (2, 4, 6, 8):
            raise ValueError("Players must be one of the following: 2, 4, 6, 8")

        self.players = []
        for i in range(int(players_size / 2)):
            self.players.extend(self.player_set(self.players))


    def random_player(self):
        return randint(0, SIZE - 1), randint(0, SIZE - 1)

    def player_exists(self, x ,y, skip):
        if not skip:
            return False

        abs_points = [math.fabs(x), math.fabs(y)]

        try:
            next((j for i in skip for j in i if math.fabs(j) in abs_points))
            return True
        except StopIteration:
            return False

    def player_set(self, skip=None):
        xa, ya = self.random_player()
        while self.player_exists(xa, ya, skip):
            xa, ya = self.random_player()
        xb, yb = -xa, -ya
        return (xa, ya), (xb, yb)


class Game(object):
    def __init__(self, players_size=4):
        self.board = Board()
        self.start()

    def start(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        try:
            self.loop(stdscr)
        except Exception as e:
            self.stop(stdscr)
            raise e
        self.stop(stdscr)

    def loop(self, stdscr):

        for x in range(1, SIZE):
            for y in range(1, SIZE):
                stdscr.addstr(int(x / 2), y, "-")
        stdscr.keypad(True)

        stdscr.refresh()
        time.sleep(5)

    def stop(self, stdscr):
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


Game()
#  python ~/PycharmProjects/python-tron/tron.py
