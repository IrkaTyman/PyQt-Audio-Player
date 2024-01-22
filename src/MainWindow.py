from PyQt5.QtWidgets import QApplication, QHBoxLayout, QStackedWidget, QSizePolicy, QVBoxLayout, QMainWindow, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from src.ui.pages.TrackPlayerPage.TrackPlayerPage import TrackPlayerPage
from src.ui.pages.SettingsPage.SettingsPage import SettingsPage
from src.ui.pages.ImportedTracksPage.ImportedTracksPage import ImportedTracksPage
from src.ui.pages.LikedTracksPage.LikedTracksPage import LikedTracksPage

from src.consts.Theme import Theme

from src.ui.components.TitleBar import TitleBar
from src.ui.components.RoundEdgesWidget import RoundEdgesWidget
from src.ui.components.NavigationPanel import NavigationPanel
from src.ui.components.Notification import Notification

class MainWindow(QMainWindow):

    def __init__(self, controller):
        super(MainWindow, self).__init__()

        self.controller = controller
        self.theme = Theme.MAIN_BLACK

        self._initWindow()
        self._initGUI()
        self._setDefaultTheme()

    def setThemeDark(self):
        self.switchTheme()
    
    def setThemeLight(self):
        self.switchTheme()

    def paintEvent(self, event):
        super().paintEvent(event)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.theme.value)
        self.setPalette(palette)

    def switchTheme(self):
        if self.theme == Theme.MAIN_BLACK:
            self.theme = Theme.MAIN_WHITE
            value = 'light'
        elif self.theme == Theme.MAIN_WHITE:
            self.theme = Theme.MAIN_BLACK
            value = 'dark'
        else:
            raise ValueError(f'Unsupported theme: {self.theme}')
        
        try:
            with open(f'styles/{value}.qss', 'r') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("QSS file not found.")

        widgets = [
            self.navigationPanel,
            self.playerView,
            self.settingsView,
            self.importView,
            self.likedView,
            self.messagePanel
        ]
        for widget in widgets:
            if isinstance(widget, RoundEdgesWidget):
                widget.switchTheme()  
            else: 
                for child in widget.findChildren(RoundEdgesWidget):
                    child.switchTheme()

        self.update()

    def _setDefaultTheme(self):
        try:
            with open('styles/dark.qss', 'r') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("QSS file not found.")

    def _initWindow(self):
        self.titleBar = TitleBar(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('resources/icons/icon.svg'))

        self.setMinimumSize(900, 700)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.theme.value)
        self.setPalette(palette)

    def _initGUI(self):
        self.navigationPanel = NavigationPanel()
        self.likedView = LikedTracksPage(self.controller)
        self.playerView =  TrackPlayerPage(self.controller)
        self.settingsView = SettingsPage(self.controller)
        self.importView = ImportedTracksPage(self.controller)
        self.messagePanel = Notification('Привет!')

        self.viewStack = QStackedWidget(self)
        self.viewStack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.viewStack.addWidget(self.playerView)
        self.viewStack.addWidget(self.importView)
        self.viewStack.addWidget(self.likedView)
        self.viewStack.addWidget(self.settingsView)
        
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.navigationPanel)
        self.horizontalLayout.addWidget(self.viewStack)
        self.horizontalLayout.setSpacing(0)
    
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 0 ,10, 10)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.messagePanel)
        self.verticalLayout.setSpacing(10)

        self.verticalBar = QVBoxLayout()
        self.verticalBar.setContentsMargins(0, 0, 0, 0)
        self.verticalBar.setSpacing(0)
        self.verticalBar.addWidget(self.titleBar)
        self.verticalBar.addLayout(self.verticalLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(self.verticalBar)
        centralWidget.setContentsMargins(0,0,0,0)
        self.setCentralWidget(centralWidget)

        self.navigationPanel.playerButton.clicked.connect(lambda: self._switchView(0))
        self.navigationPanel.importButton.clicked.connect(lambda: self._switchView(1))
        self.navigationPanel.likedButton.clicked.connect(lambda: self._switchView(2))
        self.navigationPanel.settingsButton.clicked.connect(lambda: self._switchView(3))
        
    
    def _switchView(self, index):
        self.viewStack.setCurrentIndex(index)