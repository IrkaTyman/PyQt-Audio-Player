from PyQt5.QtCore import pyqtSignal
import sqlite3
import os
from src.model.MediaData import MediaData

class Database:

    def __init__(self, dbName='music_player.db'):
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()
        self._createTable()
        self._createConfigTable()
        self.importFolder(self._getCurrentFolder())
        
    def importFolder(self, folder_path):
        if(folder_path is None):
            return
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".mp3", ".wav", ".flac", ".m4a", '.ogg')):
                    file_path = os.path.join(root, file)
                    file_path = os.path.normpath(file_path)
                    media_data = MediaData(file_path)

                    title = media_data.title
                    artist = media_data.artist
                    album_name = media_data.album
                    codec = media_data.type
                    length = media_data.length
                    
                    self._addTrack(title, artist, album_name, codec, length, file_path, liked = 0)

        self._addConfigParam(folder_path, "CurrentFolder")
    
    def getTrackByPath(self, file_path):
        self.cursor.execute("""
            SELECT * FROM Songs WHERE FilePath = ?
        """, (file_path,))
        return self.cursor.fetchone()
    
    def likeTrack(self, file_path):
        self.cursor.execute("""
            SELECT Liked FROM Songs WHERE FilePath = ?
        """, (file_path,))
        result = self.cursor.fetchone()
        if result is not None:
            current_liked_status = result[0]
            new_liked_status = 0 if current_liked_status == 1 else 1
            self.cursor.execute("""
                UPDATE Songs SET Liked = ? WHERE FilePath = ?
            """, (new_liked_status, file_path))
            self.conn.commit()
        else:
            print(f"No song found at {file_path}.")

    def getNextTrack(self, current_track_path):
        self.cursor.execute("""
            SELECT SongID FROM Songs WHERE FilePath = ?
        """, (current_track_path,))
        result = self.cursor.fetchone()
        if result is not None:
            current_track_id = result[0]
        else:
            return None

        self.cursor.execute("""
            SELECT FilePath FROM Songs WHERE SongID > ? ORDER BY SongID LIMIT 1
        """, (current_track_id,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None
        
    def getPreviousTrack(self, current_track_path):
        self.cursor.execute("""
            SELECT SongID FROM Songs WHERE FilePath = ?
        """, (current_track_path,))
        result = self.cursor.fetchone()
        if result is not None:
            current_track_id = result[0]
        else:
            return None

        self.cursor.execute("""
            SELECT FilePath FROM Songs WHERE SongID < ? ORDER BY SongID DESC LIMIT 1
        """, (current_track_id,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None 
        
    def getLikedState(self, path):
        self.cursor.execute("""
            SELECT Liked FROM Songs WHERE FilePath = ?
        """, (path,))

        result = self.cursor.fetchone()
        return result is not None and result[0] == 1
    
    def getTracks(self):
        self.cursor.execute("SELECT * FROM Songs")
        rows = self.cursor.fetchall()
        return rows

    def _createTable(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Songs (
                SongID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT,
                Artist TEXT,
                AlbumName TEXT,
                Codec TEXT,
                Length TEXT,
                FilePath TEXT UNIQUE,
                Liked INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()
    
    def _createConfigTable(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Config (
                Key TEXT,
                Value TEXT
            )
        """)
    
    def _addTrack(self, title, artist, album_name, codec, length, file_path, liked):
        self.cursor.execute("""
            SELECT SongID FROM Songs WHERE FilePath = ? OR (Title = ? AND Artist = ? AND AlbumName = ?)
        """, (file_path, title, artist, album_name, ))
        existing_song = self.cursor.fetchone()
        if existing_song:
            print(f"Song at {file_path} is already in the database.")
        else:
            self.cursor.execute("""
                INSERT INTO Songs (Title, Artist, AlbumName, Codec, Length, FilePath, Liked)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, artist, album_name, codec, length, file_path, liked, ))
            self.conn.commit()
    
    def _addConfigParam(self, key, value):
        self.cursor.execute("""
            UPDATE Config SET Value = ? WHERE Key = ?  
        """, (value, key))

    def _getCurrentFolder(self):
        self.cursor.execute("""
            SELECT Value FROM Config WHERE Key = ?
        """, ("CurrentFolder",))
        value = self.cursor.fetchone()
        return value or None

    def _close(self):
        self.conn.close()
