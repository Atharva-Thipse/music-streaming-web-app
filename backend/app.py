from typing import Optional
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import sqlite3
import os
from playlist.playlist_detail import get_playlist_details
from song.song import *
from search.search_songs import get_search_songs
from flask_caching import Cache
import redis

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(100)
UPLOAD_FOLDER = "backend\\static\\audio"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, origins='*')
ALLOWED_EXTENSIONS = ['mp3']
api = Api(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY']="music"

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client})

api.add_resource(SongResource, '/song/<int:song_id>')

'''DATABASE#######################DATABASE#######################DATABASE#######################DATABASE#######################DATABASE'''

# Function to create a database for each user
def create_user_db(user_id):
    # Define the path for the user's database
    user_db = 'backend\\static\\Users\\' + user_id + '.db'

    # Connect to the user's database
    connect_db = sqlite3.connect(user_db)
    cursor = connect_db.cursor()

    # Create the 'playlist' table if it does not exist
    cursor.execute('''    
        CREATE TABLE IF NOT EXISTS playlist (
            playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT,
            FOREIGN KEY (username) REFERENCES account(username)
        )
    ''')

    # Create the 'playlist_songs' table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlist_songs (
            playlist_id INTEGER,
            song_id INTEGER,
            FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id),
            FOREIGN KEY (song_id) REFERENCES songs(song_id),
            PRIMARY KEY (playlist_id, song_id)
        )
    ''')

    # Close the connection to the user's database
    connect_db.close()

# Function to create the main database for the music streaming application
def create_main_db():
    connect_db = sqlite3.connect('music_streaming_application.db')
    cursor = connect_db.cursor()

    # Create the 'account' table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            type TEXT NOT NULL,
            blacklisted INTEGER NOT NULL CHECK (blacklisted IN (0, 1)),
            email TEXT NOT NULL,
            visited INTEGER NOT NULL CHECK (blacklisted IN (0, 1))
        )
    ''')

    # Create the 'songs' table if it does not exist
    cursor.execute('''               
        CREATE TABLE IF NOT EXISTS songs (
            song_id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_name TEXT NOT NULL UNIQUE,
            file_path TEXT NOT NULL,
            lyrics TEXT NOT NULL,
            genre TEXT NOT NULL,
            singer TEXT NOT NULL,
            song_release_date DATE,
            album_id INTEGER,
            owner TEXT,
            avg_rating FLOAT,
            total_ratings INTEGER,
            FOREIGN KEY (album_id) REFERENCES album(album_id),
            FOREIGN KEY (owner) REFERENCES account(username)
        )
    ''')

    # Create the 'reviews' table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_id INTEGER,
            username TEXT,
            rate INTEGER,
            comments TEXT,
            FOREIGN KEY (song_id) REFERENCES songs(song_id),
            FOREIGN KEY (username) REFERENCES account(username)
        )
    ''')

    # Create the 'album' table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS album (
            album_id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_name TEXT NOT NULL,
            username TEXT,
            FOREIGN KEY (username) REFERENCES account(username)
        )
    ''')

    # Check if the admin account exists, and create it if not
    cursor.execute('SELECT * FROM account WHERE username = ?', ('admin_of_this_project',))
    if not cursor.fetchone():
        hashed_password = generate_password_hash('password_of_this_project', method='pbkdf2:sha256')
        cursor.execute('INSERT INTO account (username,password,type,blacklisted,email,visited) VALUES (?,?,?,?,?,?)', ('admin_of_this_project',hashed_password,'admin', 0, "21f3002319@ds.study.iitm.ac.in", 1))
        create_user_db('admin_of_this_project')
        connect_db.commit()
    
    connect_db.close()

# Call the function to create the main database
create_main_db()

'''########################FUNCTIONS########################FUNCTIONS########################FUNCTIONS########################FUNCTIONS'''

@app.route('/<path:filename>')
def serve_audio(filename):
    return send_from_directory('/', filename)

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to create a graph of top-rated songs
def create_graph(cursor):
    # Select top-rated songs and their average ratings from the 'songs' table
    cursor.execute('SELECT song_name, avg_rating FROM songs ORDER BY avg_rating DESC LIMIT 3')
    data = cursor.fetchall()

    # Extract labels (song names) and values (average ratings) from the data
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    # Return data as a dictionary
    return {'labels': labels, 'values': values}

def blacklist_user(username: str, blacklist: bool):
    connect_db = sqlite3.connect('music_streaming_application.db')
    cursor = connect_db.cursor()

    blacklist_str = '1' if blacklist else '0'
        
    # Update the 'blacklisted' status to 0 (whitelist) for the specified username
    cursor.execute('UPDATE account SET blacklisted = ' + blacklist_str + ' WHERE username = ?', (username,))
    connect_db.commit()
    connect_db.close()

def get_default_song():
    song = [None, '','','','','',None,None,'',None,None,None]
    return song

# Function to get the user type for a specified user
def get_user_type(user_id: str) -> str:
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Retrieve the user type from the 'account' table
        cursor.execute('SELECT type FROM account WHERE username = ?', (user_id,))
        user_type = cursor.fetchone()[0]
        connect_db.close()
        
        return user_type

# Function to get the blacklisted status for a specified user
def get_blacklisted(user_id: str) -> str:
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Retrieve the blacklisted status from the 'account' table
        cursor.execute('SELECT blacklisted FROM account WHERE username = ?', (user_id,))
        blacklisted = cursor.fetchone()[0]

        connect_db.close()
        
        return blacklisted

'''API#############API#############API#############API#############API#############API#############API#############API#############API'''

class AdminLoginValidation(Resource):
    def post(self):
        # Extract admin login credentials from the JSON request
        data = request.get_json()
        username = data.get('admin_login_username')
        password = data.get('admin_login_password')

        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Check if the provided credentials match an admin account
        cursor.execute('SELECT * FROM account WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            connect_db.close()
            access_token = create_access_token(identity={
                'username': str(user[0])
            })
            return {"message": "Login Successful", "access_token": access_token.decode('utf-8'), "user": str(user[0]), "user_type": "admin"}, 201
        else:
            connect_db.close()
            return {"error": "Incorrect password. Please try again."}, 400

api.add_resource(AdminLoginValidation, '/admin_login_validation')

class RegisterUser(Resource):
    def post(self):
        # Extract user registration details from the JSON request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM account WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return {"error": "Username already exists. Please choose a different one."}, 400

        hashed_password = generate_password_hash(password,method='pbkdf2:sha256')
        # If the username is available and passwords match, create a new user account
        cursor.execute('INSERT INTO account (username,password,type,blacklisted,email,visited) VALUES (?,?,?,?,?,?)', (username, hashed_password, 'user', 0, email,0))
        connect_db.commit()
        create_user_db(username)

        connect_db.close()

        return {"message": "User registered successfully."}, 201

api.add_resource(RegisterUser, '/register_user')

class LoginValidation(Resource):
    def post(self):
        # Extract user login credentials from the JSON request
        data = request.get_json()
        username = data.get('login_username')
        password = data.get('login_password')

        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Check if the provided username exists
        cursor.execute('SELECT * FROM account WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        # Check if the password matches the hashed password
        if user and check_password_hash(user[1], password):
            cursor.execute('UPDATE account SET visited = 1 WHERE username = ?', (user[0],))
            connect_db.commit()
            connect_db.close()
            access_token = create_access_token(identity={
                'username': str(user[0])
            })
            user_type = get_user_type(user[0])
            return {"message": "Login Successful", "access_token": access_token.decode('utf-8'), "user": str(user[0]), "user_type": str(user_type)}, 201
        else:
            connect_db.close()
            return {"error": "Incorrect password. Please try again."}, 400

api.add_resource(LoginValidation, '/login_validation')

class HomePage(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self):
        # Get the username from the JWT token
        username = get_jwt_identity()

        # Connect to the SQLite database
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Fetch the user's type from the database
        cursor.execute('SELECT type FROM account WHERE username = ?', (username['username'],))
        user_type = cursor.fetchone()[0]

        # Fetch the user's blacklisted status from the database
        cursor.execute('SELECT blacklisted FROM account WHERE username = ?', (username['username'],))
        blacklisted = cursor.fetchone()[0]

        # TODO: Decide some criteria for displaying songs. Note that there can be thousands or millions of songs
        # Fetch all songs from the database
        cursor.execute('SELECT * FROM songs')
        songs = cursor.fetchall()
        songs_json = [{'song_id': song[0], 'song_name': song[1], 'file_path': song[2], 'lyrics': song[3], 'genre': song[4], 'singer': song[5], 'song_release_date': song[6], 'album_id': song[7], 'owner': song[8], 'avg_rating': song[9], 'total_ratings': song[10]} for song in songs]

        # Fetch all albums from the database
        cursor.execute('SELECT * FROM album')
        albums = cursor.fetchall()
        albums_json = [{'album_id': album[0], 'album_name': album[1], 'username': album[2]} for album in albums]

        connect_db.close()

        # Connect to the user's personal database
        connect_db = sqlite3.connect('backend\\static\\Users\\' + username['username'] + '.db')
        cursor = connect_db.cursor()

        # Fetch all playlists for the user from the database
        cursor.execute('SELECT * FROM playlist WHERE username = ?', (username['username'],))
        playlists = cursor.fetchall()
        playlists_json = [{'playlist_id': playlist[0], 'name': playlist[1], 'username': playlist[2]} for playlist in playlists]
        
        connect_db.close()

        return {'user_type': user_type, 'playlists': playlists_json, 'albums': albums_json, 'blacklisted': blacklisted, 'songs': songs_json, 'status': 'success'}

api.add_resource(HomePage, '/home_page')

class RegisterCreator(Resource):
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Update the user type to 'creator' in the database
        cursor.execute('UPDATE account SET type = ? WHERE username = ?', ('creator', username['username']))

        connect_db.commit()
        connect_db.close()
        return {"message": "success"}, 200

api.add_resource(RegisterCreator, '/register_creator')

class CreatorPage(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self):
        username = get_jwt_identity()

        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Fetch all songs created by the user from the database
        cursor.execute('SELECT * FROM songs WHERE owner = ?', (username['username'],))
        songs = cursor.fetchall()
        songs_json = [{'song_id': song[0], 'song_name': song[1], 'file_path': song[2], 'lyrics': song[3], 'genre': song[4], 'singer': song[5], 'song_release_date': song[6], 'album_id': song[7], 'owner': song[8], 'avg_rating': song[9], 'total_ratings': song[10]} for song in songs]

        # Fetch all albums created by the user from the database
        cursor.execute('SELECT * FROM album WHERE username = ?', (username['username'],))
        albums = cursor.fetchall()
        albums_json = [{'album_id': album[0], 'album_name': album[1], 'username': album[2]} for album in albums]

        # Count the total number of songs created by the user
        cursor.execute('SELECT COUNT(*) AS total_songs FROM songs where owner = ?',(username['username'],))
        total_songs = cursor.fetchone()[0]

        # Calculate the average rating of the user's songs
        cursor.execute('SELECT AVG(avg_rating) AS average_rating FROM songs WHERE owner = ?', (username['username'],))
        average_rating = cursor.fetchone()[0]

        # Count the total number of albums created by the user
        cursor.execute('SELECT COUNT(*) FROM album WHERE username = ?', (username['username'],))
        total_albums = cursor.fetchone()[0]

        connect_db.close()
        return {'songs': songs_json, 'total_songs': total_songs, 'average_rating': average_rating, 'total_albums': total_albums, 'albums': albums_json}

api.add_resource(CreatorPage, '/creator')

class UploadSong(Resource):
    @jwt_required()
    def post(self):
        data = request.form
        # Retrieve the song file from the form data
        file = request.files['song']

        # Check if the file is valid
        if file and allowed_file(file.filename):
            # Save the file to the upload folder
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Extract song details from the form data
            args = {
                'song_name': data.get('title'),
                'lyrics': data.get('lyrics'),
                'song_genre': data.get('genre').title(),
                'song_singer': data.get('artist'),
                'release_date': data.get('releaseDate')
            }

            # Set the owner of the song to the current user
            owner = get_jwt_identity()

            # Create the new song in the database
            # Assuming SongHandler.create_song is a method that handles database operations
            # You may need to adjust this part based on your actual implementation
            # Remove "backend" from the filename
            filename = filename.replace("backend", "")
            SongHandler.create_song(args, filename, owner['username'])
            return {"message": "success"}, 200
        else:
            return {"message": "error", "error": "Choose .mp3 file extension."}, 400

api.add_resource(UploadSong, '/upload_song')

class AdminPage(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self):
        # Check if the user is logged in
        username = get_jwt_identity()
        if username:
            connect_db = sqlite3.connect('music_streaming_application.db')
            cursor = connect_db.cursor()

            # Count the total number of regular users
            cursor.execute('SELECT COUNT(*) FROM account WHERE type = "user"')
            total_users = cursor.fetchone()[0]

            # Count the total number of creators
            cursor.execute('SELECT COUNT(*) FROM account WHERE type = "creator"')
            total_creators = cursor.fetchone()[0]

            # Count the total number of songs and genres
            cursor.execute('SELECT COUNT(*) AS total_songs, COUNT(DISTINCT genre) AS total_genres FROM songs')
            result = cursor.fetchone()
            total_songs = result[0]
            total_genres = result[1]

            # Count the total number of albums
            cursor.execute('SELECT COUNT(*) FROM album')
            total_albums = cursor.fetchone()[0]

            # Call create_graph function to get data
            data = create_graph(cursor)

            connect_db.close()

            # Return the statistics as JSON
            return {'total_users': total_users, 'total_creators': total_creators, 'total_songs': total_songs, 'total_albums': total_albums, 'total_genres': total_genres, 'labels': data['labels'], 'values': data['values']}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(AdminPage, '/admin')

class UserManagement(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self):
        # Check if the user is logged in
        username = get_jwt_identity()
        if username:
            # Get the user's type (e.g., 'admin', 'creator', 'user')
            user_type = get_user_type(username['username'])

            if user_type == 'admin':
                connect_db = sqlite3.connect('music_streaming_application.db')
                cursor = connect_db.cursor()

                # Fetch the list of creators from the database
                cursor.execute('SELECT username, blacklisted FROM account WHERE type = ?', ('creator',))
                creators_list = cursor.fetchall()

                connect_db.close()

                # Return the list of creators as JSON
                return {'creators_list': creators_list}, 200
            else:
                return {"message": "error", "error": "Unauthorized access"}, 403
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(UserManagement, '/usermanagement')

class WhitelistCreator(Resource):
    @jwt_required()
    def post(self):
        # Check if the user is logged in
        username = get_jwt_identity()
        if username:
            # Extract the username from the JSON request
            data = request.get_json()
            username = data.get('username')
            blacklist_user(username, False)
            return {"message": "success"}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

class BlacklistCreator(Resource):
    @jwt_required()
    def post(self):
        # Check if the user is logged in
        username = get_jwt_identity()
        if username:
            # Extract the username from the JSON request
            data = request.get_json()
            username = data.get('username')
            blacklist_user(username, True)
            return {"message": "success"}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(WhitelistCreator, '/whitelist_creator')
api.add_resource(BlacklistCreator, '/blacklist_creator')

class TracksRecord(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self):
        username = get_jwt_identity()
        if username:
            connect_db = sqlite3.connect('music_streaming_application.db')
            cursor = connect_db.cursor()

            # Retrieve distinct genres from the 'songs' table
            cursor.execute("SELECT DISTINCT genre FROM songs")
            genres = cursor.fetchall()

            # Create a dictionary to store songs for each genre
            songs_by_genre = {}

            # Retrieve songs for each genre and store in the dictionary
            for genre in genres:
                genre_name = genre[0]
                cursor.execute("SELECT * FROM songs WHERE genre = ?", (genre_name,))
                songs = cursor.fetchall()
                songs_by_genre[genre_name] = songs
            
            connect_db.close()

            # Return the songs by genre as JSON
            return {"songs_by_genre": songs_by_genre, "searchFor": 'tracks_record'}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(TracksRecord, '/tracks')

class CreatePlaylist(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self):
        username = get_jwt_identity()
        if username:
            connect_db = sqlite3.connect('music_streaming_application.db')
            cursor = connect_db.cursor()

            cursor.execute('SELECT type FROM account WHERE username = ?', (username['username'],))
            user_type = cursor.fetchone()[0]

            #TODO: It is not good to display ALL songs to the user. There can be thousands of songs
            # Fetch all songs from the database
            cursor.execute('SELECT * FROM songs')
            songs = cursor.fetchall()

            connect_db.close()
            
            # Connect to the user's personal database
            connect_db = sqlite3.connect('backend\\static\\Users\\' + username['username'] + '.db')
            cursor = connect_db.cursor()

            # Fetch all playlists for the user from the database
            cursor.execute('SELECT playlist_id, name FROM playlist')
            playlists = cursor.fetchall()

            connect_db.close()

            return {"user_type": user_type, "searchFor": "create_playlist", "songs": songs, "playlists": playlists}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(CreatePlaylist, '/create_playlist')

class AddInPlaylist(Resource):
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        if username:
            data = request.get_json()

            # Extract data from the JSON request
            create_playlist_name = data.get('playlist_name')
            selected_songs = data.get('check_song', [])
            update_playlist_ids = data.get('check_playlist', [])

            # Check if either selected songs or playlist name/update playlist IDs are provided
            if not selected_songs or (not create_playlist_name and not update_playlist_ids):
                return {"message": "error", "error": "Invalid request"}, 400

            connect_db = sqlite3.connect('backend\\static\\Users\\' + username['username'] + '.db')
            cursor = connect_db.cursor()

            # If a new playlist is created, insert it into the 'playlist' table
            if create_playlist_name:
                cursor.execute('INSERT INTO playlist (name, username) VALUES (?, ?)', (create_playlist_name, username['username']))
                playlist_id = cursor.lastrowid
                update_playlist_ids.append(playlist_id)

            cursor.execute('SELECT * FROM playlist_songs')
            playlist_songs = cursor.fetchall()

            # Add selected songs to the selected playlists in the 'playlist_songs' table
            for playlist_id in update_playlist_ids:
                for song_id in selected_songs:
                    if (playlist_id, song_id) not in playlist_songs:
                        cursor.execute('INSERT INTO playlist_songs (playlist_id, song_id) VALUES (?, ?)', (playlist_id, song_id))

            connect_db.commit()
            connect_db.close()

            return {"message": "success"}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(AddInPlaylist, '/add_in_playlist')

#Display play list details.
class PlaylistDetails(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self, playlist_id):
        username = get_jwt_identity()
        if username:
            user_id = username['username']
            playlist_songs = get_playlist_details(user_id, playlist_id)
            user_type = get_user_type(user_id)
            blacklisted = get_blacklisted(user_id)
            return {
                "user_type": user_type,
                "playlist": playlist_songs,
                "blacklisted": blacklisted
            }, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(PlaylistDetails, '/playlist/<int:playlist_id>')
    
class AddInAlbum(Resource):
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        if username:
            data = request.get_json()

            # Extract data from the JSON request
            album_name = data.get('album_name')
            selected_songs = data.get('check_song', [])

            connect_db = sqlite3.connect('music_streaming_application.db')
            cursor = connect_db.cursor()

            # Insert the new album into the 'album' table
            cursor.execute('INSERT INTO album (album_name, username) VALUES (?, ?)', (album_name, username['username']))
            album_id = cursor.lastrowid

            # Update the 'album_id' for each selected song in the 'songs' table
            for song_id in selected_songs:
                cursor.execute('UPDATE songs SET album_id =? WHERE song_id = ?', (album_id, song_id))

            connect_db.commit()
            connect_db.close()

            return {"message": "success"}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(AddInAlbum, '/add_in_album')

class AlbumDetails(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self, album_id):
        username = get_jwt_identity()
        if username:
            user_id = username['username']
            user_type = get_user_type(user_id)
            
            connect_db = sqlite3.connect('music_streaming_application.db')
            cursor = connect_db.cursor()

            # Fetch the album name from the database
            cursor.execute('SELECT album_name FROM album WHERE album_id = ? ', (album_id,))
            album_name = cursor.fetchone()[0]

            # Fetch the songs in the album from the database
            cursor.execute('SELECT song_name, file_path, singer, song_release_date FROM songs WHERE album_id = ? ', (album_id,))
            songs = cursor.fetchall()

            connect_db.close()

            return {
                "user_type": user_type,
                "songs": [{"song_name": song[0], "file_path": song[1], "singer": song[2], "song_release_date": song[3]} for song in songs],
                "album_name": album_name,
                "blacklisted": get_blacklisted(user_id)
            }, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(AlbumDetails, '/album/<int:album_id>')

class DeleteAlbum(Resource):
    @jwt_required()
    def delete(self, album_id):
        username = get_jwt_identity()
        if username:
            connect_db = sqlite3.connect('music_streaming_application.db')
            cursor = connect_db.cursor()

            # Delete the album from the 'album' table
            cursor.execute('DELETE FROM album WHERE album_id = ?', (album_id,))
            connect_db.commit()

            # Update songs with the deleted album_id to NULL
            cursor.execute('UPDATE songs SET album_id = NULL WHERE album_id = ?', (album_id,))
            connect_db.commit()

            connect_db.close()
            return {"message": "success"}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(DeleteAlbum, '/delete_album/<int:album_id>')

class UpdateAlbum(Resource):
    @jwt_required()
    def post(self, album_id):
        username = get_jwt_identity()
        if not username:
            return {"message": "User not logged in"}, 401

        data = request.get_json()

        # Get the list of new songs and old songs from the JSON data
        new_songs = data.get('new_songs_in_album')
        old_songs = data.get('old_songs_in_album')
        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Update the album_id for each new song in the album
        if len(new_songs)>0:
            for song in new_songs:
                cursor.execute('UPDATE songs SET album_id = ? WHERE song_id = ?', (album_id, song,))
        
        # Remove the album_id for each old song in the album
        if len(old_songs)>0:
            for song in old_songs:
                cursor.execute('UPDATE songs SET album_id = NULL WHERE song_id = ?', (song,))
        
        connect_db.commit()
        connect_db.close()

        return {"success": "Album Updated Successfully"}, 200

api.add_resource(UpdateAlbum, '/edit_album/<int:album_id>')

class SongDetails(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self, song_name):
        user_id = get_jwt_identity()
        user_type = get_user_type(user_id['username'])
        blacklisted = get_blacklisted(user_id['username'])

        song = SongHandler.get_song_by_name(song_name)

        if song:
            comments = SongHandler.get_song_comments(song[0])
            return {'user_type': user_type, 'song': song, 'comments': comments, 'blacklisted': blacklisted}, 200
        else:
            return {"message": "error", "error": "Song not found"}, 404

api.add_resource(SongDetails, '/song/<string:song_name>')

class EditSong(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self, song_id):
        # Check if the user is logged in
        username = get_jwt_identity()
        if username:
            connect_db = sqlite3.connect('music_streaming_application.db')
            cursor = connect_db.cursor()

            # Retrieve current details of the selected song
            cursor.execute('SELECT * FROM songs WHERE song_id = ?', (song_id,))
            song = cursor.fetchone()

            connect_db.close()
            return {'song': song}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

    @jwt_required()
    def post(self, song_id):
        # Check if the user is logged in
        username = get_jwt_identity()
        if username:
            connect_db = sqlite3.connect('music_streaming_application.db')
            #cursor = connect_db.cursor()
            # Extract song details from the JSON request
            data = request.get_json()
            args = {
                'song_name': data.get('song_name'),
                'lyrics': data.get('lyrics'),
                'song_genre': data.get('song_genre').title(),
                'song_singer': data.get('song_singer'),
                'release_date': data.get('release_date')
            }
            # Update the song details in the database
            SongHandler.update_song(song_id, args)
            connect_db.close()
            return {"message": "success"}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(EditSong, '/edit_song/<int:song_id>')

class DeleteSong(Resource):
    @jwt_required()
    def delete(self, song_id):
        # Check if the user is logged in
        username = get_jwt_identity()
        if username:
            # Delete the specified song from the database
            SongHandler.delete_song(song_id)
            return {"message": "success"}, 200
        else:
            return {"message": "error", "error": "User not logged in"}, 401

api.add_resource(DeleteSong, '/delete_song/<int:song_id>')

@app.route('/logout_user', methods=['POST'])
@jwt_required()
def logout_user():
    resp = jsonify({'message' : 'Logged Out Successfully'})
    unset_jwt_cookies(resp)
    return resp, 200

class RateSong(Resource):
    @jwt_required()
    def post(self):
        # Retrieve user and rating information from the JSON request
        data = request.get_json()
        username = get_jwt_identity()
        song_name = data.get('song_name')
        rating = data.get('rating')

        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Retrieve the song_id for the specified song name
        cursor.execute('SELECT song_id FROM songs WHERE song_name = ?', (song_name,))
        song_id = cursor.fetchone()

        # Check if the song exists
        if song_id:
            song_id = song_id[0]

            # Check if the user has already rated the song
            cursor.execute('SELECT * FROM reviews WHERE username = ? and song_id = ?', (username['username'], song_id,))
            existing_review = cursor.fetchone()

            # Update or insert the user's rating for the song
            if existing_review:
                cursor.execute('UPDATE reviews SET rate = ? WHERE username = ? and song_id = ?', (rating, username['username'], song_id))
            else:
                cursor.execute('INSERT INTO reviews (username, song_id, rate) VALUES (?,?,?)', (username['username'], song_id, rating))

            # Calculate average rating and total ratings for the song
            cursor.execute('SELECT AVG(rate), COUNT(*) FROM reviews WHERE song_id = ?', (song_id,))
            result = cursor.fetchone()
            avg_rating = result[0]
            total_ratings = result[1]

            # Update the songs table with the calculated values
            cursor.execute('UPDATE songs SET avg_rating = ?, total_ratings = ? WHERE song_id = ?', (avg_rating, total_ratings, song_id))

            connect_db.commit()
            connect_db.close()
            return {"message": "success"}, 200
        return {"message": "error", "error": "No such song exists"}, 404

api.add_resource(RateSong, '/rate_song')

class CommentSong(Resource):
    @jwt_required()
    def post(self):
        # Retrieve user, song, and comment information from the JSON request
        data = request.get_json()
        username = get_jwt_identity()
        song_name = data.get('song_name')
        comment = data.get('comment')

        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        # Retrieve the song_id for the specified song name
        cursor.execute('SELECT song_id FROM songs WHERE song_name = ?', (song_name,))
        song_id = cursor.fetchone()

        # Check if the song exists
        if song_id:
            song_id = song_id[0]

            # Check if the user has already commented on the song
            cursor.execute('SELECT * FROM reviews WHERE username = ? and song_id = ?', (username['username'], song_id,))
            existing_review = cursor.fetchone()

            # Update or insert the user's comment for the song
            if existing_review:
                cursor.execute('UPDATE reviews SET comments = ? WHERE username = ? and song_id = ?', (comment, username['username'], song_id))
            else:
                cursor.execute('INSERT INTO reviews (username, song_id, comments) VALUES (?,?,?)', (username['username'], song_id, comment))

            # Retrieve comments for the song
            cursor.execute('SELECT * FROM reviews WHERE song_id = ?', (song_id,))
            comments = cursor.fetchall()

            connect_db.commit()
            connect_db.close()
            return {"message": "success", "comments": comments}, 200
        return {"message": "error", "error": "No such song exists"}, 404

api.add_resource(CommentSong, '/comment_song')

# Function to handle advanced search
class SearchAdv(Resource):
    @jwt_required()
    @cache.cached(timeout=2)
    def get(self):
        # Get parameters from the query string
        albumId = request.args.get('albumId')
        age = request.args.get('age')
        searchIn = request.args.get('searchIn')
        rating = request.args.get('rating')
        mySongs = request.args.get('mySongs')
        count = request.args.get('count')
        searchText = request.args.get('searchText', '')
        searchFor = request.args.get('searchFor')

        # Convert parameters to appropriate types
        rating = int(rating) if rating else 0
        count = int(count) if count else 10

        # Return the search result
        return searchAdv(searchText, searchIn, rating, count, age, mySongs == 'true', searchFor, albumId)

api.add_resource(SearchAdv, '/searchadv')

# Function to handle advanced search
@jwt_required()
def searchAdv(searchText: str, searchIn: str, rating: int, count: int, age: str, mySongs: bool, searchFor: str, albumId: Optional[int] = None):
    username = get_jwt_identity()
    connect_db = sqlite3.connect('music_streaming_application.db')
    cursor = connect_db.cursor()

    user = username['username'] if mySongs else ""

    # Get songs starting with the text
    songs1 = get_search_songs(cursor, searchText, searchIn, True, rating, user, count, age)
    songs2 = None

    if (len(searchText) > 0 and len(songs1) < count):
        # Get songs where the text is found in between (but not at the beginning)
        songs2 = get_search_songs(cursor, searchText, searchIn, False, rating, user, count - len(songs1), age)

    #merge both lists. songs where the text is found at the beginning gets priority
    songs = songs1
    if (songs2):
        songs += songs2
    
    # Extract distinct album_ids from the list of songs
    album_ids = []
    if songs and (len(songs[0])>3):
        for song in songs:
            if ((song[7] is not None) and (song[7] not in album_ids)):
                album_ids.append(song[7])

    # Fetch songs_in_album and songs_not_in_album based on album_id
    if albumId:
        cursor.execute('SELECT * FROM songs WHERE album_id = ? AND owner = ?', (albumId,user,))
        songs_in_album = cursor.fetchall()
        cursor.execute('SELECT * FROM songs WHERE album_id != ? OR album_id IS NULL AND owner = ?', (albumId,user))
        songs_not_in_album = cursor.fetchall()
    else:
        songs_in_album = []
        songs_not_in_album = []

    if (len(album_ids)==0):
        cursor.execute('SELECT album_id, album_name FROM album WHERE album_name LIKE ?', ("%"+searchText+"%",))
    else:
        cursor.execute('SELECT album_id, album_name FROM album WHERE album_id IN ({})'.format(','.join('?' for _ in album_ids)), album_ids)

    albums = cursor.fetchall()
    
    connect_db.close()
    # Determine if all songs or latest songs are being searched
    allSongs = True if (age=="all") else False

    connect_db = sqlite3.connect('backend\\static\\Users\\' + username['username'] + '.db')
    cursor = connect_db.cursor()

    # Get the list of playlists for the user
    cursor.execute('SELECT playlist_id, name FROM playlist')
    playlists = cursor.fetchall()

    connect_db.close()

    return {'allSongs': allSongs, 'searchIn': searchIn, 'searchText': searchText, 'rating': rating, 'mySongs': mySongs, 'searchFor': searchFor, 'count': count, 'user': user, 'songs': songs, 'playlists': playlists, 'albums': albums, 'songs_in_album': songs_in_album, 'songs_not_in_album': songs_not_in_album}

if __name__ == '__main__':
    app.debug = True
    app.run()