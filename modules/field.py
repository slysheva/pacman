from modules.game_states import Direction, MapCell
from modules.point import Point


class Field:
    def __init__(self, board_file):
        with open(board_file) as f:
            board = f.read().split('\n')
        self.field = [[] for i in range(len(board[0]))]
        self.width = len(board[0])
        self.height = len(board)
        self.food_cnt = 0
        map_cell = {'#': MapCell.WALL,
                    '@': MapCell.PACMAN,
                    '.': MapCell.FOOD,
                    'i': MapCell.INKY,
                    'b': MapCell.BLINKY,
                    'c': MapCell.CLYDE,
                    'p': MapCell.PINKY,
                    'o': MapCell.SPECIAL_FOOD}
        for y in range(self.height):
            for x in range(self.width):
                self.field[y].append(map_cell[board[y][x]])
                if board[y][x] == '.':
                    self.food_cnt += 1

    def cell(self, x, y):
        return self.field[y][x]

    def _move_point(self, point, direction, n=0):
        new_point = Point(X=point.X, Y=point.Y)

        if direction == Direction.RIGHT:
            new_point.X = (new_point.X + 1 + n) % self.width
        elif direction == Direction.LEFT:
            new_point.X = (new_point.X - 1 - n + self.width) \
                             % self.width
        elif direction == Direction.UP:
            new_point.Y = (new_point.Y - 1 - n + self.height) \
                             % self.height
        else:
            new_point.Y = (new_point.Y + 1 + n) % self.height
        return new_point
