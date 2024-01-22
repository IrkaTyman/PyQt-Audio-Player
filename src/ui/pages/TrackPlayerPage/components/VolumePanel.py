from PyQt5.QtWidgets import (QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QColor, QPalette

from src.ui.components.RoundButton import RoundButton
from src.ui.components.RoundEdgesWidget import RoundEdgesWidget
from src.ui.components.HorizontalSlider import HorizontalSlider

class VolumePanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self._initUI()

    def updateUI(self):
        self.volumeSlider.setValue(50)

    def _initUI(self):
        self.setAutoFillBackground(False)
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#2F2F37'))
        self.setPalette(palette)
        self.setContentsMargins(0, 0, 0, 0)

        self.hLayout = QHBoxLayout()
        self.volumeSlider = HorizontalSlider()
        self.volumeSlider.setValue(50)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)

        self.muteButton = RoundButton('resources/icons/volume-x.svg')
        self.unmuteButton = RoundButton('resources/icons/volume1.svg')

        self.hLayout.setSpacing(20)
        self.hLayout.addWidget(self.unmuteButton)
        self.hLayout.addWidget(self.volumeSlider)
        self.hLayout.addWidget(self.muteButton)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(self.hLayout)