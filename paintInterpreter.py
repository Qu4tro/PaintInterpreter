from typing import NamedTuple
from collections import defaultdict

import fileinput
import sys


white = "O"

# #################  Board   ##################


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colors = defaultdict(lambda: white)

    def hasCoordinates(self, x, y):
        return x > 0 and y > 0 and x <= self.width and y <= self.height

    def __str__(self):
        chars = []
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                chars.append(self.colors[(x, y)])
            chars.append("\n")
        return "".join(chars)


# ################# Commands ##################


class Command:
    def apply(self, board):
        return board

    @classmethod
    def from_args(cls, args):
        return cls()


class NoOp(NamedTuple, Command):
    ...


class New(NamedTuple, Command):
    width: int
    height: int

    def apply(self, board):
        # Ignore current board, since we're creating a brand new one.
        return Board(self.width, self.height)

    @classmethod
    def from_args(cls, args):
        try:
            m, n = args
            m = int(m)
            n = int(n)

            if m > 0 and n > 0:
                return cls(m, n)
            else:
                return NoOp()
        except ValueError:
            return NoOp()


class Clean(Command, NamedTuple):
    def apply(self, board):
        board.colors.clear()
        return board

    @classmethod
    def from_args(cls, args):
        return cls()


class Coloring(NamedTuple, Command):
    x: int
    y: int
    color: str

    def apply(self, board):
        board.colors[(self.x, self.y)] = self.color
        return board

    @classmethod
    def from_args(cls, args):
        try:
            x, y, color = args
            x = int(x)
            y = int(y)

            if x > 0 and y > 0:
                return cls(x, y, color)
            else:
                return NoOp()
        except ValueError:
            return NoOp()


class VerticalColoring(NamedTuple, Command):
    x: int
    y1: int
    y2: int
    color: str

    def apply(self, board):
        step = 1 if self.y1 < self.y2 else -1
        for y in range(self.y1, self.y2 + 1, step):
            board.colors[(self.x, y)] = self.color

        return board

    @classmethod
    def from_args(cls, args):
        try:
            x, y1, y2, color = args
            x = int(x)
            y1 = int(y1)
            y2 = int(y2)

            if x > 0 and y1 > 0 and y2 > 0:
                return cls(x, y1, y2, color)
            else:
                return NoOp()
        except ValueError:
            return NoOp()


class HorizontalColoring(NamedTuple, Command):
    y: int
    x1: int
    x2: int
    color: str

    def apply(self, board):
        step = 1 if self.x1 < self.x2 else -1
        for x in range(self.x1, self.x2 + 1, step):
            board.colors[(x, self.y)] = self.color

        return board

    @classmethod
    def from_args(cls, args):
        try:
            x1, x2, y, color = args
            y = int(y)
            x1 = int(x1)
            x2 = int(x2)

            if y > 0 and x1 > 0 and x2 > 0:
                return cls(y, x1, x2, color)
            else:
                return NoOp()
        except ValueError:
            return NoOp()


class FillColor(NamedTuple, Command):
    x: int
    y: int
    color: str

    def apply(self, board):
        queue = []
        queue.append((self.x, self.y))

        while queue:
            x, y = queue.pop()
            around = [
                (x - 1, y - 1),
                (x, y - 1),
                (x + 1, y - 1),
                (x - 1, y),
                (x + 1, y),
                (x - 1, y + 1),
                (x, y + 1),
                (x + 1, y + 1),
            ]
            for c in around:
                if board.hasCoordinates(*c) and board.colors[c] == board.colors[(x, y)]:
                    if c not in queue:
                        queue.append(c)

            board = Coloring(x, y, self.color).apply(board)

        return board

    @classmethod
    def from_args(cls, args):
        try:
            x, y, color = args
            x = int(x)
            y = int(y)

            if x > 0 and y > 0:
                return cls(x, y, color)
            else:
                return NoOp()
        except ValueError:
            return NoOp()


class Show(NamedTuple, Command):
    def apply(self, board):
        print(str(board))
        return board

    @classmethod
    def from_args(cls, args):
        return cls()


class Exit(NamedTuple, Command):
    def apply(self, board):
        sys.quit()

    @classmethod
    def from_args(cls, args):
        return cls()


# ################# Parsing and validating ##################


def makeCommand(line):
    char, *args = line.split()

    commandChars = {
        "I": New,
        "C": Clean,
        "L": Coloring,
        "V": VerticalColoring,
        "H": HorizontalColoring,
        "F": FillColor,
        "S": Show,
        "X": Exit,
    }

    return commandChars.get(char, NoOp).from_args(args)


# ################# Interpreter Loop ##################


def main():
    def prompt():
        print("> ", end="", flush=True)

    board = None
    prompt()
    for line in fileinput.input():
        command = makeCommand(line)
        board = command.apply(board)
        prompt()


if __name__ == "__main__":
    main()
