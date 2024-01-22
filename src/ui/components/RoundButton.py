from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QPushButton)

class RoundButton(QPushButton):

    def __init__(self, icon):
        super().__init__()
        self.tagged = False
        self.setObjectName("roundButton")

        self.setIcon(QIcon(icon))