from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QPoint, Qt, QSize

class TitleBar(QWidget):
    def __init__(self, parent = None):
        super(TitleBar, self).__init__(parent)

        self.setMaximumHeight(40)
        self._parent = parent
        self.startMovePosition = QPoint()

        self.iconLabel = QLabel(self)
        pixmap = QPixmap('resources/icons/icon.svg')
        self.iconLabel.setPixmap(pixmap)
        self.iconLabel.setMaximumSize(50,50)

        self.titleLabel = QLabel("Музыкальный плеер by Irkatyman")
        self.titleLabel.setObjectName('titleLabel')

        self.leftLayout = QHBoxLayout()
        self.leftLayout.addWidget(self.iconLabel)
        self.leftLayout.addWidget(self.titleLabel)
        self.leftLayout.setSpacing(0)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)

        self.minimizeButton = QPushButton(self)
        self.minimizeButton.setObjectName("titleButton")
        self.minimizeButton.setIcon(QIcon('resources/icons/minimize.svg'))
        self.minimizeButton.clicked.connect(self._showWindowedScreen)
        self.minimizeButton.setMaximumSize(50, 50)

        self.maximizeButton = QPushButton(self)
        self.maximizeButton.setObjectName("titleButton")
        self.maximizeButton.setIcon(QIcon('resources/icons/maximize.svg'))
        self.maximizeButton.clicked.connect(self._showFullScreen)
        self.maximizeButton.setMaximumSize(50, 50)

        self.closeButton = QPushButton(self)
        self.closeButton.setObjectName("titleButton")
        self.closeButton.setIcon(QIcon('resources/icons/close.svg'))
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setMaximumSize(50, 50)

        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(5,0,5,0)
        self.hLayout.setSpacing(15)
        self.hLayout.addLayout(self.leftLayout)
        self.hLayout.addStretch(1)
        self.hLayout.addWidget(self.minimizeButton)
        self.hLayout.addWidget(self.maximizeButton)
        self.hLayout.addWidget(self.closeButton)
        
        self.setStyleSheet('styles/dark.qss')
        self.setContentsMargins(5,0,0,5)

    def _showWindowedScreen(self):
        self._parent.showMinimized()

    def _showFullScreen(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
        else:
            self._parent.showMaximized()

    def close(self):
        self._parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startMovePosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.startMovePosition.isNull():
            diff = event.globalPos() - self.startMovePosition
            self.startMovePosition = event.globalPos()
            self._parent.move(self._parent.pos() + diff)