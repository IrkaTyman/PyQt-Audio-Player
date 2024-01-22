from PyQt5.QtWidgets import (QVBoxLayout, QSizePolicy)
from PyQt5.QtGui import QColor, QPalette

from src.ui.components.RoundButton import RoundButton
from src.ui.components.RoundEdgesWidget import RoundEdgesWidget

class NavigationPanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self._initUI()
    
    def _initUI(self):
        self.playerButton = RoundButton('resources/icons/player.svg')
        self.importButton = RoundButton('resources/icons/folder.svg')
        self.likedButton = RoundButton('resources/icons/heart.svg')
        self.settingsButton = RoundButton('resources/icons/settings.svg')

        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.playerButton)
        self.vLayout.addWidget(self.importButton)
        self.vLayout.addWidget(self.likedButton)
        self.vLayout.addStretch(1)
        self.vLayout.addWidget(self.settingsButton)

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#545463'))

        self.setPalette(palette)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.setLayout(self.vLayout)