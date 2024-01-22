from PyQt5.QtWidgets import (QLabel, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal
from QSwitchControl import SwitchControl

from src.ui.components.RoundEdgesWidget import RoundEdgesWidget

class ThemeSwitchPanel(RoundEdgesWidget):

    trackThemeChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setObjectName("SwitchPanel")

        self.text = QLabel('Переключить тему:')
        self.darkModeText = QLabel('Dark')
        self.lightModeText = QLabel('Light')
        self.switchButton = SwitchControl(active_color= "#545463")

        vLayout = QHBoxLayout()
        vLayout.addWidget(self.text)
        vLayout.addStretch(1)
        vLayout.addWidget(self.darkModeText)
        vLayout.addWidget(self.switchButton)
        vLayout.addWidget(self.lightModeText)
        self.setLayout(vLayout)

        self.switchButton.toggled.connect(self._onToggle)

    def _onToggle(self, toggled):
        if toggled: 
            self.trackThemeChanged.emit(1)
        else: 
            self.trackThemeChanged.emit(0)