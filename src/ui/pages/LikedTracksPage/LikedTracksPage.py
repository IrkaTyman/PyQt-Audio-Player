from ..ImportedTracksPage.ImportedTracksPage import ImportedTracksPage

class LikedTracksPage(ImportedTracksPage):

    def __init__(self, controller):
        super().__init__(controller)

    def removeTrack(self, filePath):
        for trackWidget in self.trackWidgets:
            if trackWidget.path == filePath:
                self.vLayout.removeWidget(trackWidget)
                trackWidget.hide()
                self.trackWidgets.remove(trackWidget)
                trackWidget.deleteLater()