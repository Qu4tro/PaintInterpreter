from typing import NamedTuple

import fileinput
import sys


def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

# #################  Board   ##################


class Board():

    default = 'O'

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.colors = {}

    def __str__(self):
        chars = []
        for y in range(1, self.height):
            for x in range(1, self.height):
                color = self.colors[(x, y)] if (x, y) in self.colors else Board.default
                chars.append(color)
            chars.append('\n')
        return "".join(chars)


# ################# Commands ##################


class New(NamedTuple):
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
                return None
        except ValueError:
            return None


class Clean(NamedTuple):
    def apply(self, board):
        board.colors.clear()
        return board

    @classmethod
    def from_args(cls, args):
        return cls()


class Coloring(NamedTuple):
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
                return None
        except ValueError:
            return None


class VerticalColoring(NamedTuple):
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
                return None
        except ValueError:
            return None


class HorizontalColoring(NamedTuple):
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
                return None
        except ValueError:
            return None


class FillColor(NamedTuple):
    x: int
    y: int
    color: str

    def apply(self, board):
        ...


class Show(NamedTuple):
    def apply(self, board):
        print(str(board))
        return board

    @classmethod
    def from_args(cls, args):
        return cls()


class Exit(NamedTuple):
    def apply(self, board):
        sys.quit()

    @classmethod
    def from_args(cls, args):
        return cls()

# ################# Parsing and validating ##################


def makeCommand(command, args):

    if command == 'I':
        return New.from_args(args)

    elif command == 'C':
        return Clean.from_args(args)

    elif command == 'L':
        return Coloring.from_args(args)

    elif command == 'V':
        return VerticalColoring.from_args(args)

    elif command == 'H':
        return HorizontalColoring.from_args(args)

    elif command == 'F':
        return FillColor.from_args(args)

    elif command == 'S':
        return Show.from_args(args)


# ################# Interpreter Loop ##################

def main():
    def prompt():
        print('> ', end='', flush=True)

    board = None
    prompt()
    for line in fileinput.input():
        commandChar, *args = line.split()
        command = makeCommand(commandChar, args)
        # print(command)
        board = command.apply(board)

        prompt()


if __name__ == '__main__':
    main()
