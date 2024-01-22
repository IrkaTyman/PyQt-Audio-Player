from PyQt5.QtWidgets import (QVBoxLayout, QLabel)
from PyQt5.QtCore import QTimer

from src.ui.components.RoundEdgesWidget import RoundEdgesWidget

class Notification(RoundEdgesWidget):

    def __init__(self, message):
        super().__init__()
        self.setObjectName("NotificationWidget")

        vLayout = QVBoxLayout()
        self.label = QLabel("")
        vLayout.addWidget(self.label)
        
        self.setLayout(vLayout)
        self.showNotification(message)

    def clearMessage(self):
        self.label.setText('')

    def showNotification(self, message, duration=3000):
        self.label.setText(message) 
        QTimer.singleShot(duration, self.clearMessage)