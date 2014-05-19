import curses
import time
from random import randint
import math

SIZE = 100

colors = [curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_RED,
          curses.COLOR_YELLOW, curses.COLOR_MAGENTA]


class Board(object):
    def __init__(self, players_size=4):
        if players_size not in (2, 4, 6):
            raise ValueError("Players must be one of the following: 2, 4, 6")

        self.board = [i for i in range(0, SIZE) for j in range(0, SIZE)]
        players = []
        for i in range(int(players_size / 2)):
            players.extend(self.player_set(players))

        self.players = [{"color": count, "points": [i]}
                        for count, i in enumerate(players)]
        print(self.players)

    def random_player(self):
        return randint(0, SIZE - 1), randint(0, SIZE - 1)


    def player_exists(self, x, y, skip):
        if not skip:
            return False

        all_points = [x, y, SIZE - x, SIZE - y]

        try:
            next((j for i in skip for j in i if math.fabs(j) in all_points))
            return True
        except StopIteration:
            return False

    def player_set(self, skip=None):
        xa, ya = self.random_player()
        while self.player_exists(xa, ya, skip):
            xa, ya = self.random_player()
        xb, yb = SIZE - xa, SIZE - ya
        return (xa, ya), (xb, yb)


class Game(object):
    def __init__(self, players_size=4):
        self.board = Board()
        self.start()

    def start(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

        for count, i in enumerate(colors):
            curses.start_color()
            curses.init_pair(count+1, i, curses.COLOR_BLACK)

        try:
            self.loop(stdscr)
        except Exception as e:
            self.stop(stdscr)
            raise e
        self.stop(stdscr)

    def loop(self, stdscr):

        for player in self.board.players:
            color = player["color"]
            for point in player["points"]:
                stdscr.addstr(int(point[0] / 2), point[1], "*", curses.color_pair(color+1))

        stdscr.keypad(True)

        stdscr.refresh()
        time.sleep(4)

    def stop(self, stdscr):
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


Game()
#  python ~/PycharmProjects/python-tron/tron.py
