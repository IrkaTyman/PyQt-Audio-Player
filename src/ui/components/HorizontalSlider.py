from PyQt5.QtWidgets import (QSlider)
from PyQt5.QtCore import Qt

class HorizontalSlider(QSlider):

    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        self.setOrientation(Qt.Horizontal)