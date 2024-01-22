from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from src.model.MediaData import MediaData

class Player(QMediaPlayer):
    
    trackCustomPositionChanged = pyqtSignal()
    trackCustomMediaChanged = pyqtSignal()
    trackCustomMediaEnd = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setVolume(50)

        self.positionChanged.connect(self._positionChanged)
        self.mediaStatusChanged.connect(self._trackStatusChanged)

    def setTrack(self, media_path):
        self.stop()
        self.setMedia(QMediaContent(QUrl.fromLocalFile(media_path)))
        self.audio = MediaData(media_path)
        self.play()
        
        self.trackCustomMediaChanged.emit()

    def _positionChanged(self, position):
        self.trackCustomPositionChanged.emit()

    def _trackStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.trackCustomMediaEnd.emit()
