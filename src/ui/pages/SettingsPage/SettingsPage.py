from PyQt5.QtWidgets import QFrame, QVBoxLayout

from .components.FolderSelectPanel import FolderSelectPanel
from .components.ThemeSwitchPanel import ThemeSwitchPanel

class SettingsPage(QFrame):

    def __init__(self, controller, parent=None):
        super().__init__(parent = parent)

        self.controller = controller
        self._initUI()
        
    def _initUI(self):
        self.importPanel = FolderSelectPanel()
        self.switchPanel = ThemeSwitchPanel()

        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(10,0,10,0)
        vLayout.addWidget(self.importPanel)
        vLayout.addStretch(1)
        vLayout.addWidget(self.switchPanel)
        self.setLayout(vLayout)