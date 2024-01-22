from PyQt5.QtWidgets import (QLabel, QHBoxLayout, QSizePolicy, QFrame)
from PyQt5.QtGui import QIcon

from src.ui.components.RoundButton import RoundButton
from src.ui.components.RoundEdgesWidget import RoundEdgesWidget
from src.ui.components.HorizontalSlider import HorizontalSlider

class PlayerPanel(RoundEdgesWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.playButton = RoundButton('resources/icons/player.svg')
        self.playButton.setEnabled(True)

        self.previousSongButton = RoundButton('resources/icons/backward.svg')
        self.previousSongButton.setEnabled(True)

        self.nextSongButton = RoundButton('resources/icons/forward.svg')
        self.nextSongButton.setEnabled(True)

        self.timeSlider = HorizontalSlider()
        self.timeSlider.setRange(0, 100)

        self.currentTime = QLabel()
        self.currentTime.setText('0:00')

        self.trackTime = QLabel()
        self.trackTime.setText('')

        hLayout = QHBoxLayout()
        hLayout.setSpacing(20)
        hLayout.addWidget(self.previousSongButton)
        hLayout.addWidget(self.playButton)
        hLayout.addWidget(self.nextSongButton)
        hLayout.addWidget(self.currentTime)
        hLayout.addWidget(self.timeSlider)
        hLayout.addWidget(self.trackTime)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(hLayout)
    
    def mediaEnd(self):
        self.currentTime.setText("0:00")
        self.timeSlider.setDisabled(True)
        self.timeSlider.setValue(0)
        self.previousSongButton.setDisabled(True)
        self.nextSongButton.setDisabled(True)
        self.playButton.setDisabled(True)
        self.playButton.setIcon(QIcon('resources/icons/play.svg'))

    def updateUI(self, length):
        self.currentTime.setText("0:00")
        self.trackTime.setText(str(length))
        self.timeSlider.setDisabled(False)
        self.timeSlider.setValue(0)
        self.previousSongButton.setDisabled(False)
        self.nextSongButton.setDisabled(False)
        self.playButton.setDisabled(False)
        self.playButton.setIcon(QIcon('resources/icons/pause.svg'))