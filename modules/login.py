from PyQt5.QtCore import QSize, QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton

from modules.pacman_game import PacmanWindow


class Communicate(QObject):
    closeApp = pyqtSignal()


class LoginWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setFixedSize(QSize(360, 140))
        self.setWindowTitle("Enter your name")
        self.setStyleSheet(
            'background-color: #0FB321;border-style: outset;'
            'font: bold 14px;min-width: 10em;padding: 6px;')
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        self.dialog = PacmanWindow()

        self.run_game = Communicate()
        self.run_game.closeApp.connect(self.return_from_game)
        self.dialog.give(self.run_game.closeApp)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200, 42)
        pybutton.setStyleSheet(
            'background-color: #EFEC1F;border-style: outset;border-width:'
            ' 7px;border-radius: 200px;border-color:'
            ' black;font: bold 14px;min-width: 10em;padding: 6px;')
        pybutton.move(80, 60)

    def clickMethod(self):
        user = self.line.text()
        self.dialog.run(user)
        self.hide()

    def run(self):
        self.show()

    def give(self, signal):
        self.signal = signal

    def return_from_game(self):
        self.signal.emit()
        self.close()
