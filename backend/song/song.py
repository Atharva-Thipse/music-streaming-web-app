import sqlite3
from flask_restful import reqparse, Resource

class SongHandler:
    # Static method to get a song by its ID
    @staticmethod
    def get_song(song_id):
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()
        cursor.execute('SELECT * FROM songs WHERE song_id = ?', (song_id,))
        song = cursor.fetchone()
        connect_db.close()
        return song

    # Static method to update a song's information
    @staticmethod
    def update_song(song_id, args):
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()
        cursor.execute('''
            UPDATE songs
            SET song_name = ?, lyrics = ?, genre = ?, singer = ?, song_release_date = ?
            WHERE song_id = ?
        ''', (args['song_name'], args['lyrics'], args['song_genre'], args['song_singer'], args['release_date'], song_id))
        connect_db.commit()
        connect_db.close()

    # Static method to create a new song
    @staticmethod
    def create_song(args, file_path, owner):
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()
        cursor.execute('''
            INSERT INTO songs (song_name, file_path, lyrics, genre, singer, song_release_date, owner)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (args['song_name'], file_path, args['lyrics'], args['song_genre'], args['song_singer'], args['release_date'], owner))
        connect_db.commit()
        connect_db.close()

    # Static method to delete a song by its ID
    @staticmethod
    def delete_song(song_id):
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()
        cursor.execute('DELETE FROM songs WHERE song_id = ?', (song_id,))
        connect_db.commit()
        connect_db.close()
    
    # Static method to get a song by its name
    @staticmethod
    def get_song_by_name(song_name):
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()
        cursor.execute('SELECT * FROM songs WHERE song_name = ?', (song_name,))
        song = cursor.fetchone()
        connect_db.close()
        return song

    # Static method to get comments for a song by its ID
    @staticmethod
    def get_song_comments(song_id):
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()
        cursor.execute('SELECT * FROM reviews WHERE song_id = ?', (song_id,))
        comments = cursor.fetchall()
        connect_db.close()
        return comments

# Resource class for handling RESTful operations on a song
class SongResource(Resource):
    # Get method to retrieve information about a song by its ID
    def get(self, song_id):
        song = SongHandler.get_song(song_id)
        if song:
            return {'status': 'success', 'song': {'id': song[0], 'name': song[1], 'singer': song[5], 'genre': song[4], 'release_date': song[6], 'lyrics': song[3]}}
        else:
            return {'status': 'error', 'message': 'Song not found'}, 404

    # Put method to update information about a song by its ID
    def put(self, song_id):
        parser = reqparse.RequestParser()
        parser.add_argument('song_name', type=str, help='Song name is required')
        parser.add_argument('lyrics', type=str)
        parser.add_argument('song_genre', type=str)
        parser.add_argument('song_singer', type=str)
        parser.add_argument('release_date', type=str, help='Release date is required')
        args = parser.parse_args()
        SongHandler.update_song(song_id, args)
        return {'status': 'success', 'message': 'Song updated successfully'}

    # Post method to create a new song
    def post(self, song_id):
        parser = reqparse.RequestParser()
        parser.add_argument('song_name', type=str, help='Song name is required')
        parser.add_argument('lyrics', type=str)
        parser.add_argument('song_genre', type=str)
        parser.add_argument('song_singer', type=str)
        parser.add_argument('release_date', type=str, help='Release date is required')
        args = parser.parse_args()
        SongHandler.create_song(args)
        return {'status': 'success', 'message': 'Song created successfully'}

    # Delete method to delete a song by its ID
    def delete(self, song_id):
        SongHandler.delete_song(song_id)
        return {'status': 'success', 'message': 'Song deleted successfully'}