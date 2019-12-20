from ADgame1 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Widget(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def __del(self):
        pass

    def initUI(self):
        self.setGeometry(100, 100, 400, 700)
        self.setWindowTitle('슈팅 게임')
        self.setFixedSize(self.rect().size())
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(0, 0, 0))
        self.setPalette(palette)

        self.game = PlayGame(self)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.game.draw(qp)
        qp.end()

    def keyPressEvent(self, e):
        self.game.keyDown(e.key())

    def closeEvent(self, e):
        self.game.exitGame()