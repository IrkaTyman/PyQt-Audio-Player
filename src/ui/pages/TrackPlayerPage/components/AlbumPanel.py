from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSignal

from src.ui.components.RoundButton import RoundButton
from src.ui.components.RoundEdgesWidget import RoundEdgesWidget

class AlbumPanel(RoundEdgesWidget):
        
        trackLiked = pyqtSignal(bool)

        def __init__(self, controller):
            super().__init__()

            self.controller = controller
            self._initUI(None)

        def updateUI(self, audio, value):
            self._setAlbumCover(audio.getAlbumCover(), 250)
            if value:
                self._setLikedButtonStyles()
                self.likeButton.tagged = True
            else: 
                self._setDefaultButtonStyles()
                self.likeButton.tagged = False

        def _initUI(self, audio):
            self.albumCover = QLabel()
            if audio != None: 
                self._setAlbumCover(audio.getAlbumCover(), 250)
            else: 
                self._setDefaultCover(250)

            self.likeButton = RoundButton('resources/icons/heart.svg')
            self.likeButton.setEnabled(False)
            self.likeButton.clicked.connect(self._likeClick)
            self.likeButton.tagged = False

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setXOffset(5)
            shadow.setYOffset(5)
            shadow.setColor(Qt.black)
            shadow.setColor(QColor(0, 0, 0, 80)) 
            self.albumCover.setGraphicsEffect(shadow)

            self.spacer1 = QSpacerItem(20, 40, QSizePolicy.MinimumExpanding)
            self.spacer2 = QSpacerItem(20, 40, QSizePolicy.MinimumExpanding)

            hLayout = QHBoxLayout()  
            hLayout.addItem(self.spacer1)
            hLayout.addWidget(self.albumCover)
            hLayout.addItem(self.spacer2)

            h2Layout = QHBoxLayout()
            h2Layout.addItem(self.spacer1)
            h2Layout.addWidget(self.likeButton)
            h2Layout.addItem(self.spacer2)

            vLayout = QVBoxLayout()
            vLayout.setContentsMargins(0,0,0,20)
            vLayout.addLayout(hLayout)
            vLayout.addLayout(h2Layout)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.setLayout(vLayout)

        def _setAlbumCover(self, data, ratio):
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            if pixmap.isNull():
                fallback_path = 'resources/no_media.png'
                pixmap.load(fallback_path)

            pixmap = pixmap.scaled(ratio, ratio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.albumCover.setPixmap(pixmap)
            
        def _setDefaultCover(self, ratio):
            pixmap = QPixmap()
            fallback_path = 'resources/no_media.png'
            pixmap.load(fallback_path)
            pixmap = pixmap.scaled(ratio, ratio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.albumCover.setPixmap(pixmap)

        def _likeClick(self):
            self.likeButton.tagged = not self.likeButton.tagged

            if self.likeButton.tagged:
                self.trackLiked.emit(True)
                self._setLikedButtonStyles()
                self.controller.logMessage('Песня добавлена в избранные')
            else: 
                self.trackLiked.emit(False)
                self._setDefaultButtonStyles()
                self.controller.logMessage('Песня удалена из избранных')
            
        def _setLikedButtonStyles(self):
            self.likeButton.setStyleSheet(
                """
                QPushButton {
                    background-color: #BFe80c5c;  
                    border-radius: 25px; 
                    min-width: 50px; 
                    max-width: 50px; 
                    min-height: 50px; 
                    max-height: 50px;
                }
                QPushButton:hover {
                    background-color: #66e80c5c
                }
                QPushButton:pressed {
                    background-color: #80B34467;
                }
            """)
                
        def _setDefaultButtonStyles(self):
            self.likeButton.setStyleSheet("""
                QPushButton {
                    background-color: #B3e06089;  
                    border-radius: 25px; 
                    min-width: 50px; 
                    max-width: 50px; 
                    min-height: 50px; 
                    max-height: 50px;
                }
                QPushButton:hover {
                    background-color: #66e06089;
                }
                QPushButton:pressed {
                    background-color: #38717184;
                }
                """)