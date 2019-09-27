import os

from PyQt5 import QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QColor
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QMainWindow

from modules import game_painter


class PacmanWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def give(self, signal):
        self.signal = signal

    def initUI(self):

        self.board = game_painter.GameActions(self)

        self.statusbar = self.statusBar()
        self.board.ScoreSignal[str].connect(self.statusbar.showMessage)

        self.init_width = self.width()
        self.init_height = self.height()
        self.setWindowTitle('Pacman')

        self.setAutoFillBackground(True)
        p = self.palette()
        self.setStyleSheet(
            'background-color: #0FB321;border-style: outset;'
            'font: bold 14px;min-width: 10em;padding: 6px;')
        self.setPalette(p)

    def run(self, user):
        self.board = game_painter.GameActions(self)

        self.statusbar = self.statusBar()
        self.board.ScoreSignal[str].connect(self.statusbar.showMessage)
        self.player = QMediaPlayer()
        curr = os.getcwd()
        sound = QtMultimedia.QMediaContent(QUrl.fromLocalFile(
            os.path.join(curr, "music", "pacman_beginning.wav")))
        self.player.setMedia(sound)
        self.player.play()
        self.player.setVolume(60)

        self.show()
        board = self.board
        board.start(user)

        self.setCentralWidget(board)

        self.resize(board.curr_game.board.width * board.scale,
                    (board.curr_game.board.height + 4) * board.scale)

    def resizeEvent(self, event):
        self.board.resizeEvent_(self.init_width, self.init_height,
                                self.width(), self.height())

    def keyPressEvent(self, e):
        self.board.keyPressEvent(e)

    def closeEvent(self, *args, **kwargs):
        self.signal.emit()
