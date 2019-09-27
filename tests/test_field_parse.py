import sys

import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import unittest

from modules import game_states
from modules.field import Field


class FieldParseCase(unittest.TestCase):
    def test_field_pars_works_well(self):
        try:
            field = Field("tests\\test_board.txt")
        except Exception as e:
            field = Field("test_board.txt")

        self.assertEqual(field.cell(0, 0), game_states.MapCell.FOOD)
        self.assertEqual(field.cell(0, 1), game_states.MapCell.WALL)
        self.assertEqual(field.cell(1, 0), game_states.MapCell.PACMAN)
        self.assertEqual(field.cell(2, 0), game_states.MapCell.BLINKY)
        self.assertEqual(field.cell(1, 1), game_states.MapCell.INKY)
        self.assertEqual(field.cell(2, 1), game_states.MapCell.CLYDE)
        self.assertEqual(field.cell(3, 1), game_states.MapCell.PINKY)


if __name__ == '__main__':
    unittest.main()
