import sys

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication

from modules.login import LoginWindow
from modules.records_table import TableWindow


class Communicate(QObject):
    closeApp = pyqtSignal()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.pushButton = QPushButton("Start game!", self)
        self.pushButtonTable = QPushButton("Game records", self)
        self.setFixedSize(730, 430)
        self.pushButton.resize(230, 80)
        self.pushButtonTable.resize(230, 80)
        self.pushButton.move(235, 120)
        self.pushButtonTable.move(235, 240)
        bold = QFont("Times", 18, QFont.Bold)
        self.pushButton.setFont(bold)
        self.pushButton.setStyleSheet(
            'background-color: #EFEC1F;border-style: outset;border-width:'
            ' 7px;border-radius: 200px;border-color:'
            ' black;font: bold 14px;min-width: 10em;padding: 6px;')

        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButtonTable.clicked.connect(self.on_pushButtonTable_clicked)
        self.pushButtonTable.setStyleSheet(
            'background-color: #EFEC1F;border-style: outset;border-width:'
            ' 7px;border-radius: 200px;border-color:'
            ' black;font: bold 14px;min-width: 10em;padding: 6px;')
        self.setStyleSheet(
            'background-color: #0FB321;border-style: outset;'
            'font: bold 14px;min-width: 10em;padding: 6px;')
        self.dialog = LoginWindow()
        self.dialog_table = TableWindow()

        self.close_table = Communicate()
        self.close_table.closeApp.connect(self.run)
        self.dialog_table.give(self.close_table.closeApp)

        self.login_game = Communicate()
        self.login_game.closeApp.connect(self.run)
        self.dialog.give(self.login_game.closeApp)

    def on_pushButtonTable_clicked(self):
        self.dialog_table.run()
        self.hide()

    def on_pushButton_clicked(self):
        self.dialog.run()
        self.hide()

    def run(self):
        self.show()


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.run()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
