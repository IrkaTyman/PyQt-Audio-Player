import os
import io
from PyQt5.QtCore import pyqtSignal, QObject
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

from src.lib.convertSeconds import convertSeconds

class MediaData(QObject):

    trackErrorOccured = pyqtSignal(str)

    def __init__(self, filepath):
        QObject.__init__(self)
        
        self.filepath = filepath
        self.title = 'Без названия'
        self.audio = None
        self.artist = 'Неизвестно'
        self.album = 'Неизвестно'
        self.type = 'Неизвестно'
        self.length = 0
        self.artwork = None
        self.hasСover = False
        self._getAudioMetadata()

    def getAlbumCover(self):
        if self.hasСover and self.type == 'm4a':
            return self.audio['covr'][0]
        elif self.hasСover and self.type == 'mp3':
            return next((tag.data for tag in self.audio.tags.values() if tag.FrameID == 'APIC'), None)
        elif self.hasСover and self.type == 'flac':
            return next((picture.data for picture in self.audio.pictures if picture.type == 3), None)
        
    def _getAudioMetadata(self):
        fileExtension = os.path.splitext(self.filepath)[1].lower()

        try:
            if fileExtension == '.mp3':
                self._getMP3Metadata(self.filepath)
            elif fileExtension == '.flac':
                self._getFlacMetadata(self.filepath)
            elif fileExtension == '.wav':
                self._getWavMetadata(self.filepath)
            elif fileExtension == '.m4a':
                self._getM4AMetadata(self.filepath)
        except Exception as e:
            self.trackErrorOccured.emit(str(f'Ошибка при обработке файла: {self.filepath}, error: {e}'))
             
    def _getMP3Metadata(self, filepath):
        self.audio = MP3(filepath, ID3=ID3)
        self.title = self.audio.get("TIT2", "Без названия")[0]
        self.artist = self.audio.get('TPE1', ['Неизвестно'])[0]
        self.album = self.audio.get('TALB', ['Неизвестно'])[0]
        self.type = 'mp3'
        self.length = convertSeconds(self.audio.info.length)

        self.hasСover = False
        if self.audio.tags is not None:
            for tag in self.audio.tags.values():
                if tag.FrameID == 'APIC':
                    self.hasСover = True
                    break

    def _getFlacMetadata(self, filepath):
        self.audio = FLAC(filepath)
        self.title = self.audio.get("title", ["No Title"])[0]
        self.artist = self.audio.get('artist', ['Unknown'])[0]
        self.album = self.audio.get('album', ['Unknown'])[0]
        self.type = 'flac'
        self.length = convertSeconds(self.audio.info.length)

        self.hasСover = len(self.audio.pictures) > 0
        
    def _getWavMetadata(self, filepath):
        self.audio = mutagen.File(filepath)
        self.length = convertSeconds(self.audio.info.length)
        self.title = 'Unknown'
        self.artist = 'Unknown'
        self.album = 'Unknown'
        self.hasСover = False

    def _getM4AMetadata(self, filepath):
        self.audio = MP4(filepath)
        self.type = 'm4a'
        self.title = self.audio.get("\xa9nam", ["No Title"])[0]
        self.length = convertSeconds(self.audio.info.length)
        self.artist = self.audio.get('\xa9ART', ['Unknown'])[0]
        self.album = self.audio.get('\xa9alb', ['Unknown'])[0]
        self.hasСover = 'covr' in self.audio