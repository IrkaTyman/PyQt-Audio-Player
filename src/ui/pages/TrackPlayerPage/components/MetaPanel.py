from PyQt5.QtWidgets import (QLabel, QSizePolicy, QGridLayout, QFrame)

from src.ui.components.RoundEdgesWidget import RoundEdgesWidget

class MetaPanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        self.trackTitleLabel = QLabel(f"Название: ")
        self.artistNameLabel = QLabel(f"Исполнитель: ")
        self.albumNameLabel = QLabel(f"Альбом: ")
        self.lengthLabel = QLabel(f"Продолжительность: ")
        self.codecLabel = QLabel(f"Файл: ")

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setLineWidth(2)

        layout = QGridLayout()
        layout.addWidget(self.trackTitleLabel, 0, 0)
        layout.addWidget(self.artistNameLabel, 0, 1)
        layout.addWidget(self.albumNameLabel, 0, 2)
        layout.addWidget(self.lengthLabel, 2, 0)
        layout.addWidget(self.codecLabel, 2, 1)
        layout.addWidget(self.separator, 1, 0, 1, 4)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(layout)

    def updateUI(self, audio):
        self.trackTitleLabel.setText(f"Название: {audio.title}")
        self.artistNameLabel.setText(f"Исполнитель: {audio.artist}")
        self.albumNameLabel.setText(f"Альбом: {audio.album}")
        self.lengthLabel.setText(f"Продолжительность: {audio.length}")
        self.codecLabel.setText(f"Файл: {audio.type}")