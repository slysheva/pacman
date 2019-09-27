import time

from PyQt5 import QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer
from modules.game_events import GameEvents
import os


class MusicExecuter():
    def __init__(self):
        curr = os.getcwd()
        self.events = set()
        self.main_player = QMediaPlayer()
        self.player = QMediaPlayer()
        self.music_files = {
            GameEvents.FOOD_EATEN: os.path.join(
                curr,
                "music",
                "pacman_chomp.wav"),
            GameEvents.APPLE_EATEN: os.path.join(
                curr,
                "music",
                "pacman_eatfruit.wav"),
            GameEvents.GHOST_EATEN: os.path.join(
                curr,
                "music",
                "pacman_eatghost.wav"),
            GameEvents.PACMAN_DEATH: os.path.join(
                curr,
                "music",
                "pacman_death.wav"),
            GameEvents.INTERMITION: os.path.join(
                curr,
                "music",
                "pacman_intermission.wav"),
            GameEvents.NEW_LEVEL: os.path.join(
                curr,
                "music",
                "pacman_beginning.wav"),
            GameEvents.NEW_LIVE: os.path.join(
                curr,
                "music",
                "pacman_extrapac.wav")}

    def add_events(self, events):
        for event in events:
            self.events.add(event)

    def play_music(self):
        for event in self.events:
            sound = QtMultimedia.QMediaContent(
                QUrl.fromLocalFile(self.music_files[event]))
            if (event == GameEvents.INTERMITION
                    or event == GameEvents.NEW_LEVEL
                    or event == GameEvents.NEW_LIVE):
                self.main_player.setMedia(sound)
                self.main_player.play()
                self.main_player.setVolume(60)
            else:
                self.player.setMedia(sound)
                self.player.play()
                self.player.setVolume(60)
            if event == GameEvents.PACMAN_DEATH:
                time.sleep(2)

        self.events.clear()
