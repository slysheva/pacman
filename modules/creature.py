
from abc import ABCMeta, abstractmethod, abstractproperty


class Creature:
    def __init__(self, pos, name):
        self._pos = pos
        self._name = name
        self.last_pos = pos
        self.init_pos = pos

    @abstractmethod
    def make_step(self, field):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, s):
        self._name = s

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self.last_pos = self._pos
        self._pos = pos
