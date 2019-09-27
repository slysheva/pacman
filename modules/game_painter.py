import os
import time

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtWidgets import QFrame

from modules import game_building, game_logic
from modules.game_events import GameEvents
from modules.game_states import MonstersState, MapCell
from modules.music_executer import MusicExecuter


class GameActions(QFrame):
    ScoreSignal = pyqtSignal(str)

    def __init__(self, parent):
        self.user = ''
        self.music_executer = MusicExecuter()
        super().__init__(parent)
        self.timer = QBasicTimer()
        self.timerOn = False
        self.speed = 80
        self.scale = 20
        self.game = game_building.GameStarter()
        self.curr_game = self.game.game_instance
        self.step = 1
        self.MAX_STEP = 4
        self.QP = QPainter()
        self.directions = {game_logic.Direction.RIGHT: "right",
                           game_logic.Direction.LEFT: "left",
                           game_logic.Direction.UP: "up",
                           game_logic.Direction.DOWN: "down"}

    def timerEvent(self, event):
        if self.step == 1:
            self.curr_game.game_step()
            events = self.curr_game.get_events()
            self.music_executer.add_events(events)

            if GameEvents.PACMAN_DEATH in events:
                time.sleep(2)

        self.ScoreSignal.emit(str(self.curr_game.score))
        self.game_over()
        self.curr_game = self.game.game_instance
        self.update()

    def start(self, user):
        self.user = user
        self.timer.start(self.speed, self)
        self.timerOn = True

    def pause(self):
        if self.timerOn:
            self.timer.stop()
        else:
            self.timer.start(self.speed, self)

        self.timerOn = not self.timerOn

    def paintEvent(self, QP):
        QP = QPainter()
        QP.begin(self)
        try:
            self.drawBoard(QP)
        except Exception as e:
            self.game = game_building.GameStarter()
            self.curr_game = self.game.game_instance
        finally:
            QP.end()
        self.increase()

    def increase(self):
        if self.step == self.MAX_STEP:
            self.step = 1
            return
        if self.step == 2:
            self.music_executer.play_music()

        self.step += 1

    def drawBoard(self, QP):
        def get_path(file_name):
            return os.path.join("images", file_name)

        def get_pos(curr, prev):
            delta = (curr - prev) * (self.step / self.MAX_STEP)
            if abs(curr - prev) > 1:
                delta = 0
            return prev + delta

        QP.setBrush(QColor(0, 150, 0))
        for y in range(self.curr_game.board.height):
            for x in range(self.curr_game.board.width):
                if self.curr_game.board.cell(x, y) == MapCell.WALL:
                    QP.setBrush(QColor(0, 0, 100))
                    QP.drawRect(x * self.scale,
                                y * self.scale, self.scale, self.scale)
                if self.curr_game.board.cell(x, y) == MapCell.FOOD:
                    pixmap = QPixmap(get_path("imageApple"))
                    QP.drawPixmap(x * self.scale + self.scale / 4,
                                  y * self.scale + self.scale / 4,
                                  self.scale / 2, self.scale / 2, pixmap)
                if self.step % 4 != 0:
                    if self.curr_game.board.cell(x, y) == MapCell.SPECIAL_FOOD:
                        pixmap = QPixmap(get_path("imageApple"))
                        QP.drawPixmap(x * self.scale,
                                      y * self.scale,
                                      self.scale, self.scale, pixmap)
        for y in range(self.curr_game.board.height):
            for x in range(self.curr_game.board.width):
                if self.curr_game.board.cell(x, y) == MapCell.PACMAN:
                    QP.setBrush(QColor(250, 218, 94))
                    y_ = get_pos(self.curr_game.pacman.pos.Y,
                                 self.curr_game.pacman.last_pos.Y) * self.scale
                    dir = self.curr_game.pacman.direction
                    if self.step % 4 != 0:
                        pixmap = QPixmap(
                            os.path.join(get_path("pacman{}_{}".format(
                                self.step % 4,
                                self.directions[dir]))))
                    else:
                        pixmap = QPixmap(get_path("pacman4"))
                    QP.drawPixmap(get_pos(
                        self.curr_game.pacman.pos.X,
                        self.curr_game.pacman.last_pos.X) * self.scale,
                                  y_,
                                  self.scale, self.scale, pixmap)
                for monster in self.curr_game.monsters:
                    if game_logic.Point(X=x, Y=y) == monster.pos:
                        pixmap = QPixmap(monster.image)
                        if monster.state == MonstersState.FRIGHTENED:
                            pixmap = QPixmap(get_path("FRIGHTENED"))
                        QP.drawPixmap(get_pos(
                            monster.pos.X,
                            monster.last_pos.X) * self.scale,
                            get_pos(
                                monster.pos.Y,
                                monster.last_pos.Y) * self.scale,
                            self.scale,
                            self.scale, pixmap)
            pixmap = QPixmap(get_path("live"))
            for i in range(3):
                if self.curr_game.lives > (2 - i):
                    QP.drawPixmap((self.curr_game.board.width - (3 - i) * 2)
                                  * self.scale,
                                  self.curr_game.board.height * self.scale,
                                  self.scale * 1.5, self.scale * 1.5, pixmap)

    def commit_users_result(self):
        users = []
        with open("result_table.txt") as f:
            for line in f.read().split('\n'):
                if line:
                    data = line.split(' ')
                    users.append((data[0], int(data[1]), int(data[2])))
        users.append((self.user, self.game.curr_level, self.curr_game.score))
        users = sorted(users, key=lambda a: a[2])
        users = reversed(users)
        with open("result_table.txt", 'w') as f:
            for i, user in enumerate(users):
                if i < 7:
                    print(user[0] + ' ' + str(user[1]) + ' ' + str(user[2]),
                          file=f)

    def game_over(self):
        if self.curr_game.lives == 0:
            self.timer.stop()
            self.timerOn = False
            self.ScoreSignal.emit(
                'Game Over you got ' + str(self.curr_game.score)
                + ' scores!!!')
            self.commit_users_result()
        elif not self.curr_game.game_active:
            self.game.update_level()

    def resizeEvent_(self, width, height, current_width, current_height):
        times = min(current_height / height, current_width / width)
        times = max(times, 1)
        self.scale = 20 * times

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_P:
            self.pause()
        elif key == Qt.Key_Right:
            self.curr_game.pacman.next_step = game_logic.Direction.RIGHT
        elif key == Qt.Key_Left:
            self.curr_game.pacman.next_step = game_logic.Direction.LEFT
        elif key == Qt.Key_Up:
            self.curr_game.pacman.next_step = game_logic.Direction.UP
        elif key == Qt.Key_Down:
            self.curr_game.pacman.next_step = game_logic.Direction.DOWN
