from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtGui import QIcon

from src.lib.convertSeconds import convertSeconds
from src.ui.components.RoundEdgesWidget import RoundEdgesWidget

from .components.PlayerPanel import PlayerPanel
from .components.VolumePanel import VolumePanel
from .components.AlbumPanel import AlbumPanel
from .components.MetaPanel import MetaPanel

class TrackPlayerPage(QFrame):

    def __init__(self, controller, parent = None):
        super().__init__(parent= parent)
        self.controller = controller
        self._initUI()

    def positionChanged(self, currentTime, length):
        self.playerPanel.currentTime.setText(convertSeconds(int(currentTime))) 
        if length != 0: 
            percentagePlayed = (currentTime / length) * 100
            self.playerPanel.timeSlider.setValue(int(percentagePlayed))
        if length == 0: self.playerPanel.timeSlider.setValue(0)

    def mediaChanged(self, audio, value):
        self.playerPanel.updateUI(audio.length)
        self.albumPanel.updateUI(audio, value)
        self.metaPanel.updateUI(audio)
        self.volumePanel.updateUI()

    def switchTheme(self):
        for child in self.findChildren(RoundEdgesWidget):
            child.switchTheme()

    def _play(self):
        if self.controller.isPlaying():
            self.controller.stopPlaying()
            self.playerPanel.playButton.setIcon(QIcon('resources/icons/play.svg'))
        else:
            self.controller.startPlaying()
            self.playerPanel.playButton.setIcon(QIcon('resources/icons/pause.svg'))

    def _playPreviousSong(self):
        self.controller.getPreviousTrack()

    def _playNextSong(self):
        self.controller.getNextTrack()

    def _setPosition(self, position):
        self.controller.setPosition(position)
        currentTime = self.controller.requestPlayerTime() / 1000
        self.playerPanel.currentTime.setText(convertSeconds(int(currentTime))) 

    def _mute(self):
        self.controller.muteAudio(True)
        self.volumePanel.volumeSlider.setSliderPosition(0)
        self.controller.logMessage("Звук выключен")

    def _unmute(self):
        self.controller.muteAudio(False)
        if self.volumePanel.volumeSlider.value() <= 90:
            self.volumePanel.volumeSlider.setValue(self.volumePanel.volumeSlider.value() + 10)

        self.controller.logMessage("Звук включен")
        
    def _setVolume(self, volume):
        iconPath = 'resources/icons/volume0.svg'
        if volume > 50:
            iconPath = 'resources/icons/volume2.svg'
        elif volume > 20:
            iconPath = 'resources/icons/volume1.svg'
    
        self.volumePanel.unmuteButton.setIcon(QIcon(iconPath))

        self.controller.muteAudio(False)
        self.controller.setVolume(volume)
        self.controller.logMessage(f"Громкость: {volume}%")
    
    def _timeSliderPressed(self):
        self.playerPanel.timeSlider.sliderMoved.disconnect(self._setPosition)
    
    def _timeSliderReleased(self):
        self._setPosition(self.playerPanel.timeSlider.value())
        self.playerPanel.timeSlider.sliderMoved.connect(self._setPosition)

    def _initUI(self):
        self.playerPanel = PlayerPanel()
        self.volumePanel = VolumePanel()
        self.albumPanel = AlbumPanel(self.controller)
        self.metaPanel = MetaPanel()

        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(10,0,0,0)
        vLayout.addWidget(self.albumPanel)
        vLayout.addWidget(self.metaPanel)
        vLayout.addWidget(self.volumePanel)
        vLayout.addWidget(self.playerPanel)
        self.setLayout(vLayout)

        self.playerPanel.playButton.clicked.connect(self._play)
        self.playerPanel.previousSongButton.clicked.connect(self._playPreviousSong)
        self.playerPanel.nextSongButton.clicked.connect(self._playNextSong)
        self.playerPanel.timeSlider.sliderMoved.connect(self._setPosition)
        self.playerPanel.timeSlider.sliderPressed.connect(self._timeSliderPressed)
        self.playerPanel.timeSlider.sliderReleased.connect(self._timeSliderReleased)

        self.volumePanel.muteButton.clicked.connect(self._mute)
        self.volumePanel.unmuteButton.clicked.connect(self._unmute)
        self.volumePanel.volumeSlider.valueChanged.connect(self._setVolume)