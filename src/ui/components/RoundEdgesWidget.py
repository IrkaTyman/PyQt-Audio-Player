from PyQt5.QtWidgets import (QWidget)
from src.consts.Theme import Theme
from PyQt5.QtGui import QPainterPath, QPainter, QRegion
from PyQt5.QtCore import Qt

class RoundEdgesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = Theme.BLACK

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.theme.value)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
    
    def switchTheme(self):
        if self.theme == Theme.BLACK:
            self.theme = Theme.WHITE
        elif self.theme == Theme.WHITE:
            self.theme = Theme.BLACK
        else:
            raise ValueError(f'Тема не поддерживается: {self.theme}')
        
        self.update()