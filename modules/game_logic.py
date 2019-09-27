import os
import random

from modules.game_events import GameEvents
from modules.game_states import MonstersState, MapCell, CreatureType, Direction
from modules.monster import Monster
from modules.pacman import Pacman
from modules.point import Point


class Game:

    def parse_monsters_and_pacman(self):
        def get_path(file_name):
            return os.path.join("images", file_name)

        pacman_cords = None
        monsters = set()

        for y in range(self.board.height):
            for x in range(self.board.width):
                if self.board.cell(x, y) == MapCell.PACMAN:
                    pacman_cords = Point(x, y)
                elif self.board.cell(x, y) == MapCell.INKY:
                    monsters.add(Monster(Point(x, y),
                                         get_path("inky"),
                                         Point(X=23, Y=13),
                                         CreatureType.INKY))
                elif self.board.cell(x, y) == MapCell.BLINKY:
                    monsters.add(Monster(Point(x, y),
                                         get_path("blinky"),
                                         Point(X=21, Y=-2),
                                         CreatureType.BLINKY))
                elif self.board.cell(x, y) == MapCell.PINKY:
                    monsters.add(Monster(Point(x, y),
                                         get_path("pinky"),
                                         Point(X=1, Y=-2),
                                         CreatureType.PINKY))
                elif self.board.cell(x, y) == MapCell.CLYDE:
                    monsters.add(Monster(Point(x, y),
                                         get_path("clyde"),
                                         Point(X=1, Y=13),
                                         CreatureType.CLYDE))
        return pacman_cords, monsters

    def __init__(self, board, score=0, lives=3):
        self.game_on = True
        self.score = score
        self.lives = lives
        self.events = []
        self.game_active = True
        self.board = board
        pacman_coords, self.monsters = self.parse_monsters_and_pacman()

        self.foodCnt = self.board.food_cnt
        self.init_pos = pacman_coords
        self.iter = 1
        self.timer = 1
        self.pacman = Pacman(pacman_coords, CreatureType.PACMAN,
                             Direction.RIGHT)
        self.monster_state = MonstersState.CHASE

    def _update_monsters_chase_state(self):
        new_monsters = set()

        for monster in self.monsters:
            self._update_monster_state()
            if monster.name == CreatureType.BLINKY:
                monster.target = self.pacman.pos
            elif monster.name == CreatureType.PINKY:
                monster.target = self.board._move_point(
                    self.pacman.pos,
                    self.pacman.direction, 4)
            elif monster.name == CreatureType.INKY:
                monster.target = self.board._move_point(
                    self.pacman.pos,
                    self.pacman.direction, 2)
                monster.target.X += monster.target.X - self.pacman.pos.X
                monster.target.Y += monster.target.Y - self.pacman.pos.Y
            else:
                if monster.pos.find_dist_sq(self.pacman.pos) > 64:
                    monster.target = self.pacman.pos
                else:
                    monster.target = monster.scatter_point

            new_monsters.add(monster)

        self.monsters = new_monsters

    def _update_monsters_scatter_state(self):

        new_monsters = set()

        for monster in self.monsters:
            monster.target = monster.scatter_point
            new_monsters.add(monster)

        self.monsters = new_monsters

    def _update_monsters_frightened_state(self):

        new_monsters = set()

        for monster in self.monsters:
            if self.timer == self.iter + 20 - 1:
                monster.target = monster.last_pos
                monster.last_pos = Point(0, 0)
            else:
                possible = []
                for delta_x in range(-1, 2):
                    for delta_y in range(-1, 2):
                        target = Point(monster.pos.X + delta_x,
                                       monster.pos.Y + delta_y)
                        if (abs(delta_x) == abs(delta_y)
                                or target == monster.last_pos):
                            continue
                        possible.append(target)
                if possible:
                    index = random.randint(0, len(possible) - 1)
                    monster.target = possible[index]

            new_monsters.add(monster)

        self.monsters = new_monsters

    def _update_monsters(self):
            self._update_monster_state()
            if self.monster_state == MonstersState.CHASE:
                self._update_monsters_chase_state()
            elif self.monster_state == MonstersState.SCATTER:
                self._update_monsters_scatter_state()
            else:
                self._update_monsters_frightened_state()

    def is_pacman_caught(self):
        for monster in self.monsters:
            if (self.pacman.pos == monster.pos
                or (self.pacman.pos == monster.last_pos
                    and self.pacman.last_pos == monster.pos)):
                return True
        return False

    def _collect_food_pacman(self, point):

        if MapCell.FOOD == self.board.cell(point.X, point.Y):
            self.foodCnt -= 1
            self.score += 1
            self.events.append(GameEvents.FOOD_EATEN)
            self.board.field[point.Y][point.X] = MapCell.EMPTY
        if MapCell.SPECIAL_FOOD == self.board.cell(point.X, point.Y):
            self._update_monster_state(True)
            self.events.append(GameEvents.INTERMITION)
            self.board.field[point.Y][point.X] = MapCell.EMPTY

    def _monster_go_to_init(self, monster):

        self.monsters.remove(monster)
        monster.pos = monster.init_pos
        monster.last_pos = monster.init_pos
        monster.next_pos = monster.init_pos
        monster.update_state(MonstersState.CHASE)
        self.monsters.add(monster)

    def update_game_state(self):
        if self.score % 200 == 0 and self.lives < 3:
            self.lives += 1
            self.events.append(GameEvents.NEW_LIVE)
        point = self.pacman.pos
        self._collect_food_pacman(point)

        if self.foodCnt == 0:
                self.game_active = False
                self.events.append(GameEvents.NEW_LEVEL)

        if self.is_pacman_caught():
                for monster in self.monsters:
                        if (monster.pos == self.pacman.pos
                                or (self.pacman.pos == monster.last_pos
                                    and self.pacman.last_pos == monster.pos)):
                            if monster.state == MonstersState.FRIGHTENED:
                                self.events.append(GameEvents.GHOST_EATEN)

                                self._monster_go_to_init(monster)
                            else:
                                self.events.append(GameEvents.PACMAN_DEATH)
                                self.lives -= 1
                                self.pacman.pos = self.init_pos
                                self._restart_level()

    def _update_monster_state(self, frightened=False):
        if frightened:
            self.monster_state = MonstersState.FRIGHTENED
            self.timer = self.iter + 20
        elif (self.monster_state == MonstersState.FRIGHTENED
              and self.timer > self.iter):
            return
        elif ((self.iter % 25 == 0 or self.iter <= self.timer)
              and self.iter < 100):
            self.monster_state = MonstersState.SCATTER
            if self.timer == 0:
                self.timer = self.iter + 7
            if self.iter == self.timer:
                self.timer = 0
        else:
            self.timer = 0
            self.monster_state = MonstersState.CHASE
        for monster in self.monsters:
            monster.update_state(self.monster_state)

    def check(self):
        def is_bad(some_monster):
            case1 = self.pacman.pos == some_monster.last_pos
            case2 = self.pacman.last_pos == some_monster.pos
            return case1 and case2

        for monster in self.monsters:
            if is_bad(monster):
                self.pacman.pos = self.pacman.last_pos

    def get_events(self):
        for event in self.events:
            yield event
        self.events.clear()

    def game_step(self):
        self.events = []
        self.update_game_state()

        self.iter += 1
        self.pacman.make_step(self.board)
        self._update_monsters()
        new_monsters = set()
        for monster in self.monsters:
            monster.make_step(self.board)
            new_monsters.add(monster)
        self.monsters = new_monsters
        self.check()

    def _restart_level(self):
        for monster in self.monsters:
            self._monster_go_to_init(monster)
