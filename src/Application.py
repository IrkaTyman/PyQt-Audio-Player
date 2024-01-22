import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from src.MainWindow import MainWindow
from src.config.Database import Database
from src.config.Player import Player
from src.config.Controller import Controller

class Application(QApplication):

    def __init__(self, argv):
        QApplication.__init__(self, argv)

        self.controller = Controller()

        self.db = Database()
        self.controller.setDB(self.db)

        self.window = MainWindow(self.controller)
        self.controller.setWindow(self.window)

        # media = QMediaPlayer()
        # media.setMedia(QMediaContent(QUrl.fromLocalFile(r"C:\Users\ellia\OneDrive\Рабочий стол\Simplified-Audio-main\resources\Lady Gaga - Bad romance.mp3")))
        # media.play()
        
        self.player = Player()
        self.controller.setMedia(self.player)
        
        self.window.show()
        sys.exit(self.exec_())