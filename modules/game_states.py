from enum import Enum


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class MapCell(Enum):
    PACMAN = 0
    EMPTY = 1
    FOOD = 2
    WALL = 3
    INKY = 4
    BLINKY = 5
    PINKY = 6
    CLYDE = 7
    SPECIAL_FOOD = 8


class MonstersState(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2


class CreatureType(Enum):
    INKY = 0
    BLINKY = 1
    CLYDE = 2
    PINKY = 3
    PACMAN = 4
