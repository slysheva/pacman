from enum import Enum


class GameEvents(Enum):
    FOOD_EATEN = 0
    GHOST_EATEN = 1
    NEW_LIVE = 2
    PACMAN_DEATH = 3
    APPLE_EATEN = 4
    INTERMITION = 5
    NEW_LEVEL = 6
