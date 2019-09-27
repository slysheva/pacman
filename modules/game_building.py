from modules import game_logic
import os

from modules.field import Field


class GameStarter:
    def __init__(self):
        with open(os.path.join("levels", "description.txt")) as f:
            self.levels = f.read().split('\n')
        self.curr_level = 0
        field = Field(os.path.join("levels", self.levels[self.curr_level]))
        self.game_instance = game_logic.Game(field, 0)

    def update_level(self):
            self.curr_level += 1
            if self.curr_level < len(self.levels):
                field = Field(
                    os.path.join("levels", self.levels[self.curr_level]))
                self.game_instance = game_logic.Game(
                    field, self.game_instance.score, self.game_instance.lives)
