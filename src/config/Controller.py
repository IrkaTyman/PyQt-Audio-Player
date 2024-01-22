from src.model.MediaData import MediaData
import os
from PyQt5.QtMultimedia import QMediaPlayer
    
class Controller:
     
    def __init__(self):
        pass
    
    def isPlaying(self):
        return True if self.media.state() == QMediaPlayer.PlayingState else False
    
    def stopPlaying(self):
        self.media.pause()
    
    def startPlaying(self):
        self.media.play()
    
    def setPosition(self, position):
        self.media.setPosition(int(position * self.media.duration() / 100))

    def requestPlayerTime(self):
        return self.media.position()
    
    def muteAudio(self, bool):
        self.media.setMuted(bool)
    
    def setVolume(self, volume):
        self.media.setVolume(volume)
        
    def requestLoadTrack(self, path):
        self.media.setTrack(path)
        self.setVolume(50)
        self.window.playerView.albumPanel.likeButton.setEnabled(True)
        self.window.playerView.mediaChanged(self.media.audio, self.db.getLikedState(path))

        self.window.messagePanel.showNotification(f'Включили песню из папки {path}')
    
    def getNextTrack(self):
        nextSong = self.db.getNextTrack(self.media.audio.filepath)
        if nextSong is not None:
            self.media.setTrack(nextSong)
            self.window.playerView.mediaChanged(self.media.audio, self.db.getLikedState(self.media.audio.filepath))
    
    def getPreviousTrack(self):
        prevSong = self.db.getPreviousTrack(self.media.audio.filepath)
        if prevSong is not None:
            self.media.setTrack(prevSong)
            self.window.playerView.mediaChanged(self.media.audio, self.db.getLikedState(self.media.audio.filepath))

    def logMessage(self, message):
        self.window.messagePanel.showNotification(message, 3000)

    def changePosition(self):
        self.window.playerView.positionChanged(self.media.position() / 1000 , self.media.duration() / 1000)

    def setWindow(self, window):
        self.window = window
        self._musicFolderChanged('music_player.db')
        self._addLikedTracksToScreen()

        self.window.settingsView.importPanel.trackFolderChanged.connect(self._musicFolderChanged)
        self.window.settingsView.switchPanel.trackThemeChanged.connect(self._onThemeChanged)

        self.window.playerView.albumPanel.trackLiked.connect(self._trackLiked)

    def setDB(self, db):
        self.db = db
    
    def setMedia(self, mediaPlayer):
        self.media = mediaPlayer
        self.media.trackCustomPositionChanged.connect(self.changePosition)
        self.media.trackCustomMediaEnd.connect(self._onMediaEnd)

    def _musicFolderChanged(self, path):
        self.db.importFolder(path)

        self.db.cursor.execute("SELECT * FROM Songs")
        allTracks = self.db.cursor.fetchall()

        self._clearLayout(self.window.importView.scrollAreaLayout)

        for track in allTracks:
            id = track[0]
            title = track[1]
            artist = track[2]
            albumName = track[3]
            codec = track[4]
            length = track[5]
            filePath = track[6]
            liked = track[7]

            data = MediaData(filePath)
            data = data.getAlbumCover()
            self.window.importView.addTrack(data, title, artist, albumName, codec, length, filePath)

        self.window.messagePanel.showNotification(f'Импортировано из папки: {path}')
    
    def _addLikedTracksToScreen(self):
        allTracks = self.db.getTracks()

        for track in allTracks:
            id = track[0]
            title = track[1]
            artist = track[2]
            albumName = track[3]
            codec = track[4]
            length = track[5]
            filePath = track[6]
            liked = track[7]

            if liked:
                data = MediaData(filePath)
                data = data.getAlbumCover()
                self.window.likedView.addTrack(data, title, artist, albumName, codec, length, filePath)
    
    def _addLikedTrack(self, filePath):
        track = self.db.getTrackByPath(filePath)

        if track:
            title = track[1]
            artist = track[2]
            albumName = track[3]
            codec = track[4]
            data = MediaData(filePath)
            data = data.getAlbumCover()
            length = track[6]

            self.window.likedView.addTrack(data, title, artist, albumName, codec, length, filePath)
    
    def _removedLikedTrack(self, filePath):
        self.window.likedView.removeTrack(self.media.audio.filepath)

    def _trackLiked(self, value):
        self.db.likeTrack(self.media.audio.filepath)

        if value:
            self._addLikedTrack(self.media.audio.filepath)
        else: 
            self._removedLikedTrack(self.media.audio.filepath)

    def _onThemeChanged(self, value):
        if value == 1: self.window.setThemeLight()
        else: self.window.setThemeDark()

    def _onMediaEnd(self):
        self.window.playerView.playerPanel._onMediaEnd() 

    def _clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if item.widget() is not None:
                widget = item.widget()
                layout.removeWidget(widget)
                widget.deleteLater()

            elif item.layout() is not None:
                self._clearLayout(item.layout())
                layout.removeItem(item)
                item.deleteLater()
   
