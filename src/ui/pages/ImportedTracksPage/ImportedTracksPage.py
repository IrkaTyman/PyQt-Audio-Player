from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QFrame
from PyQt5.QtCore import Qt

from src.ui.components.RoundEdgesWidget import RoundEdgesWidget

from .components.TrackWidget import TrackWidget

class ImportedTracksPage(QFrame):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.trackWidgets = []
        self._initUI()

    def addTrack(self, data, title, artist, album, codec, length, path):
        self.trackWidget = TrackWidget(data, title, artist, album, codec, length, path)
        self.trackWidgets.append(self.trackWidget)
        self.trackWidget.trackSelected.connect(self._onTrackSelected)
        self.scrollAreaLayout.addWidget(self.trackWidget)

    def _onTrackSelected(self, path):
        self.controller.requestLoadTrack(path)

    def _initUI(self):
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidget.setObjectName("ScrollArea")
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidget)
        self.scrollAreaLayout.setAlignment(Qt.AlignTop)
        self.scrollAreaWidget.setLayout(self.scrollAreaLayout)

        self.qscroll = QScrollArea()
        self.qscroll.setWidgetResizable(True)
        self.qscroll.setWidget(self.scrollAreaWidget)
        self.qscroll.setFrameShape(QFrame.NoFrame)

        self.mainWidget = RoundEdgesWidget()
        self.mainLayout = QVBoxLayout(self.mainWidget)
        self.mainLayout.addWidget(self.qscroll)
        self.mainLayout.setContentsMargins(10,10,10,10) 
        self.mainWidget.setLayout(self.mainLayout)

        self.vLayout = QVBoxLayout()
        self.vLayout.setContentsMargins(10,0,0,0)
        self.vLayout.addWidget(self.mainWidget)

        self.setLayout(self.vLayout)
