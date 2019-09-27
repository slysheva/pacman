from modules.creature import Creature
from modules.game_states import MonstersState, MapCell
from modules.point import Point


class Monster(Creature):
    def __init__(self, current_pos, image, scatter_point, name):
        super().__init__(current_pos, name)
        self.pos = current_pos
        self.image = image
        self.target = Point(X=0, Y=0)
        self.scatter_point = scatter_point
        self.last_pos = self.pos
        self.state = MonstersState.CHASE

    def update_state(self, state):
        self.state = state

    def make_step(self, board):
        min_dis = (board.width * board.height + 1)\
                  * (board.width * board.height + 1)
        best_point = self.last_pos
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_pos = Point(
                    X=(self.pos.X + i + board.width) % board.width,
                    Y=(self.pos.Y + j + board.height) % board.height)
                x = new_pos.X
                y = new_pos.Y
                is_wall = board.cell(x, y) == MapCell.WALL
                is_same = self.last_pos == new_pos
                is_frigh = self.state != MonstersState.FRIGHTENED
                is_change = is_same and is_frigh
                if abs(i) == abs(j) or is_change or is_wall:
                    continue
                dist = new_pos.find_dist_sq(self.target)
                if dist < min_dis:
                    min_dis = dist
                    best_point = new_pos
        self.last_pos = self.pos
        self.pos = best_point
