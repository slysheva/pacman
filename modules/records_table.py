from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QGridLayout,\
    QWidget, QTableWidget, QTableWidgetItem


class TableWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setStyleSheet(
            'background-color: #0FB321')
        self.setFixedSize(QSize(380, 270))
        self.setWindowTitle("Records")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)
        self.table = None
        self.load_data()

    def give(self, signal):
        self.signal = signal

    def load_data(self):
        if self.table is not None:
            self.layout.removeWidget(self.table)
        else:
            self.table = QTableWidget(self)
            self.table.setColumnCount(3)
            self.table.setRowCount(7)

        self.table.setHorizontalHeaderLabels(["USER", "LEVELS", "SCORE"])

        for i in range(
                self.table.columnCount()):
            self.table.horizontalHeaderItem(i).\
                setTextAlignment(Qt.AlignHCenter)

        self.table.horizontalHeaderItem(0).setFlags(QtCore.Qt.ItemIsEnabled)
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(i, j, item)
        with open("result_table.txt", 'r') as f:
            content = f.read().split('\n')
        for i, line in enumerate(content):
            if i < 7 and line:
                data = line.split(' ')
                user = QTableWidgetItem(data[0])
                user.setFlags(QtCore.Qt.ItemIsEnabled)
                user.setFont(QtGui.QFont("Fantasy", 10, QtGui.QFont.Bold))
                level = QTableWidgetItem(data[1])
                level.setFlags(QtCore.Qt.ItemIsEnabled)
                score = QTableWidgetItem(data[2])
                score.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(i, 0, user)
                self.table.setItem(i, 1, level)
                self.table.setItem(i, 2, score)

        self.table.resizeColumnsToContents()

        self.layout.addWidget(self.table, 0, 0)
        self.setCentralWidget(self.central_widget)

    def run(self):
        self.load_data()
        self.table.setStyleSheet(
            'background-color: #EFEC1F;border-style: outset;'
            ' border-color:'
            ' black;font: bold 10px')

        self.show()

    def closeEvent(self, event):
        self.signal.emit()
