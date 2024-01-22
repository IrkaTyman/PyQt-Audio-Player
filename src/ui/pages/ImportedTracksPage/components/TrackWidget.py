from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QSizePolicy, QFrame)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

class TrackWidget(QWidget):

    trackSelected = pyqtSignal(str)

    def __init__(self, data, title, artist, album, codec, length, path):
        super().__init__()
        self.setObjectName('TrackWidget')

        self.coverArtLabel = QLabel(self)
        pixmap = QPixmap()
        if data != None:
            pixmap.loadFromData(data)
        if pixmap.isNull():
            fallback_path = 'resources/no_media.png'
            pixmap.load(fallback_path)

        pixmap = pixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.coverArtLabel.setPixmap(pixmap)

        self.titleLabel = QLabel(title[:20])
        self.artistLabel = QLabel(artist[:20])
        self.albumLabel = QLabel(album[:20])
        self.codecLabel = QLabel(codec[:20])
        self.lengthLabel = QLabel(length[:20])
        self.path = path

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,5)
        self.layout.addWidget(self.coverArtLabel)
        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(self.artistLabel)
        self.layout.addWidget(self.albumLabel)
        self.layout.addWidget(self.codecLabel)
        self.layout.addWidget(self.lengthLabel)

        self.setLayout(self.layout)

        labels = [self.titleLabel, self.artistLabel, self.albumLabel, self.codecLabel, self.lengthLabel]
        for label in labels:
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
    def mousePressEvent(self, event):
        self.trackSelected.emit(self.path)
