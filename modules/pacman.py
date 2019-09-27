from modules.creature import Creature
from modules.game_states import MapCell


class Pacman(Creature):
    def __init__(self, pos, name, direction):
        super().__init__(pos, name)
        self._next_step = None
        self._direction = direction

    def make_step(self, board):
        self.last_pos = self.pos
        new_position = board._move_point(self.pos,
                                         self.direction)
        if self.next_step is not None:
            next_position = board._move_point(self.pos,
                                              self.next_step)
            if board.cell(next_position.X,
                          next_position.Y) != MapCell.WALL:
                self.pos = next_position
                self.direction = self.next_step
                self.next_step = None
            elif board.cell(new_position.X,
                            new_position.Y) != MapCell.WALL:
                self.pos = new_position
        elif board.cell(new_position.X,
                        new_position.Y) != MapCell.WALL:
            self.pos = new_position

    @property
    def next_step(self):
        return self._next_step

    @next_step.setter
    def next_step(self, next_step):
        self._next_step = next_step

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direct):
        self._direction = direct
