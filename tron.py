import curses
import time
from random import randint
import math

SIZE = 100

colors = [curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_RED,
          curses.COLOR_YELLOW, curses.COLOR_MAGENTA]

horizontal = ["LEFT", "RIGHT"]
vertical = ["UP", "DOWN"]
directions = horizontal + vertical

possible_directions = {i: vertical for i in horizontal}
possible_directions.update({i: horizontal for i in vertical})


class Player(object):
    def __init__(self, color, points, direction=None):
        self.color = color
        self.points = points
        self.direction = direction or directions[randint(0, 3)]


class FairRandom(object):
    @classmethod
    def make_random_players(cls, player_size):
        players = []
        for i in range(int(player_size / 2)):
            new_players = cls.player_set(players)
            # If any of players already exist make new ones
            while [i for i in new_players if i in players]:
                new_players = cls.player_set(players)

            players.extend(new_players)

        return [Player(count, [points]) for count, points in enumerate(players)]

    @classmethod
    def random_player(cls):
        return randint(0, SIZE - 1), randint(0, SIZE - 1)

    @classmethod
    def player_set(cls, skip=None):
        xa, ya = cls.random_player()
        xb, yb = SIZE - xa, SIZE - ya
        return (xa, ya), (xb, yb)


class Board(object):
    def __init__(self, players=None, player_size=2):
        if player_size not in (2, 4, 6):
            raise ValueError("Players must be one of the following: 2, 4, 6")

        self.board = [i for i in range(0, SIZE) for j in range(0, SIZE)]
        self.players = players or FairRandom.make_random_players(player_size)


class Game(object):
    def __init__(self, players_size=4):
        self.board = Board()
        self.start()

    def start(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        for count, i in enumerate(colors):
            curses.start_color()
            curses.init_pair(count + 1, i, curses.COLOR_BLACK)

        try:
            self.loop(stdscr)
        except Exception as e:
            self.stop(stdscr)
            raise e
        self.stop(stdscr)

    def loop(self, stdscr):

        for player in self.board.players:
            color = curses.color_pair(player.color)
            for point in player.points:
                stdscr.addstr(int(point[0] / 2), point[1], "*", color)

        stdscr.keypad(True)

        stdscr.refresh()
        time.sleep(4)

    def stop(self, stdscr):
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


Game()
# python ~/PycharmProjects/pytron/tron.py
