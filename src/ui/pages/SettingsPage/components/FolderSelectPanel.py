from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QSpacerItem, QFrame, QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

from src.ui.components.RoundButton import RoundButton
from src.ui.components.RoundEdgesWidget import RoundEdgesWidget

class FolderSelectPanel(RoundEdgesWidget):

    trackFolderChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.path = 'resources\extracted'
        self._initUI()

    def _initUI(self):
        icon = QIcon('resources/icons/folder.svg')
        pixmap = icon.pixmap(20, 20) 
        self.iconLabel = QLabel(self)
        self.iconLabel.setPixmap(pixmap)

        self.text = QLabel('Импортировать музыку из папки', self)
        self.text.setObjectName("PathSelectPanelLabel")

        self.button = RoundButton(QIcon('resources/icons/folder-plus.svg'))
        self.button.clicked.connect(self._onClick)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.pathLabel = QLabel('',self)
        
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.pathLabel)
        vLayout.addWidget(self.line)

        hTopLayout = QHBoxLayout()
        hTopLayout.setSpacing(10)
        hTopLayout.addWidget(self.iconLabel)
        hTopLayout.addWidget(self.text)

        horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hBottomLayout = QHBoxLayout()
        hBottomLayout.addStretch(1)
        hBottomLayout.addLayout(vLayout)
        hBottomLayout.addItem(horizontalSpacer)
        hBottomLayout.addStretch(1)

        hMainLayout = QHBoxLayout()
        hMainLayout.setSpacing(5)
        hMainLayout.addLayout(hTopLayout)
        hMainLayout.addLayout(hBottomLayout)
        hMainLayout.addWidget(self.button)
        self.setLayout(hMainLayout)

    def _onClick(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderPath = QFileDialog.getExistingDirectory(self,"Выберите папку", "", options=options)
        if folderPath:
            self.pathLabel.setText(f'Папка: {folderPath}')
            self.path = folderPath

            self.trackFolderChanged.emit(self.path)