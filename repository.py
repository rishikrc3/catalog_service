import sqlite3
class Repository:
    def __init__(self, table):
        self.table = table
        self.database = self.table + ".db"
        self.make()
    
    def make(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS tracks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, artist TEXT NOT NULL);")
            connection.commit()
    
    def insert(self, title, artist):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO tracks (title, artist) VALUES (?, ?)", (title, artist))
            connection.commit()
            return cursor.lastrowid
        
    def get(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, title, artist FROM tracks")
            return cursor.fetchall()
        
    def delete_track(self, track_id):  
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tracks WHERE id = ?", (track_id,))
            connection.commit()
            return cursor.rowcount > 0  