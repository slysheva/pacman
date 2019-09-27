import sys

import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import unittest

from modules.field import Field
from modules.game_logic import Game
from modules.game_states import CreatureType, MonstersState
from modules.point import Point

TEST_FIELD = "tests\\test_board.txt"


class GameLogicTests(unittest.TestCase):
    def setUp(self):
        try:
            self.field = Field(TEST_FIELD)
        except Exception as e:
            self.field = Field('test_board.txt')
        self.game = Game(self.field)

    def test_parse_monsters_and_pacman_works_well(self):
        coords, monsters = self.game.parse_monsters_and_pacman()

        self.assertEqual(coords, Point(1, 0))

        for monster in monsters:
            if monster.name == CreatureType.INKY:
                self.assertEqual(monster.scatter_point, Point(X=23, Y=13))
            elif monster.name == CreatureType.BLINKY:
                self.assertEqual(monster.scatter_point, Point(X=21, Y=-2))
            elif monster.name == CreatureType.PINKY:
                self.assertEqual(monster.scatter_point, Point(X=1, Y=-2))
            elif monster.name == CreatureType.CLYDE:
                self.assertEqual(monster.scatter_point, Point(X=1, Y=13))

    def test_update_monsters_chase_state(self):
        self.game.game_step()
        monsters = self.game.monsters
        for monster in monsters:
            if monster.name == CreatureType.INKY:
                self.assertEqual(monster.target, Point(X=-2, Y=0))
            elif monster.name == CreatureType.BLINKY:
                self.assertEqual(monster.target, Point(X=2, Y=0))
            elif monster.name == CreatureType.PINKY:
                self.assertEqual(monster.target, Point(X=2, Y=0))
            elif monster.name == CreatureType.CLYDE:
                self.assertEqual(monster.scatter_point, Point(X=1, Y=13))

    def test_update_monsters_frightened_state(self):
        self.game.game_step()
        self.game._update_monster_state(True)

        self.game.game_step()

        monsters = self.game.monsters
        for monster in monsters:
            if monster.name == CreatureType.INKY:
                self.assertEqual(monster.target, Point(X=1, Y=1))
            elif monster.name == CreatureType.BLINKY:
                self.assertEqual(monster.target, Point(X=2, Y=0))
            elif monster.name == CreatureType.PINKY:
                self.assertEqual(monster.target, Point(X=3, Y=1))
            elif monster.name == CreatureType.CLYDE:
                self.assertEqual(monster.scatter_point, Point(X=1, Y=13))

    def test_update_monsters_scatter_state(self):
        self.game.game_step()
        self.game.monster_state = MonstersState.SCATTER

        self.game.game_step()

        monsters = self.game.monsters
        for monster in monsters:
            if monster.name == CreatureType.INKY:
                self.assertEqual(monster.target, Point(X=-2, Y=0))
            elif monster.name == CreatureType.BLINKY:
                self.assertEqual(monster.target, Point(X=2, Y=0))
            elif monster.name == CreatureType.PINKY:
                self.assertEqual(monster.target, Point(X=2, Y=0))
            elif monster.name == CreatureType.CLYDE:
                self.assertEqual(monster.scatter_point, Point(X=1, Y=13))

    def test_restart_level(self):
        self.game.game_step()
        self.game._restart_level()

        monsters = self.game.monsters
        for monster in monsters:
            if monster.name == CreatureType.INKY:
                self.assertEqual(monster.last_pos, Point(X=1, Y=1))
            elif monster.name == CreatureType.BLINKY:
                self.assertEqual(monster.last_pos, Point(X=2, Y=0))
            elif monster.name == CreatureType.PINKY:
                self.assertEqual(monster.last_pos, Point(X=3, Y=1))
            elif monster.name == CreatureType.CLYDE:
                self.assertEqual(monster.last_pos, Point(X=2, Y=1))


if __name__ == '__main__':
    unittest.main()
