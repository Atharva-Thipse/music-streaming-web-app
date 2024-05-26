import sqlite3

'''
Get songs details for a playlist identified by user id and playlist id
TODO: Maybe playlist id can be converted to a string represented as <user id>-<playlist no>
'''
def get_playlist_details(user_id: str, playlist_id: int) -> list:
        #Get Play list name and song ids using play list id from User DB

        #1. Get PLaylsit name
        connect_db = sqlite3.connect('backend\\static\\Users\\' + user_id + '.db')
        cursor = connect_db.cursor()
        cursor.execute('''
                SELECT name FROM playlist
                WHERE playlist_id = ?
                ''', (playlist_id,))
        playlist_name = cursor.fetchone()[0]

        #2. Get song ids for the play list
        cursor.execute('''
                SELECT song_id FROM playlist_songs
                WHERE playlist_id = ?
                ''', (playlist_id,))

        playlist_song_ids = cursor.fetchall()
        connect_db.close()

        if (len(playlist_song_ids)==0):
              return []
        
        #3. Get song details from song ids from Main DB
        playlist_song_ids_str = "("
        for song_id in playlist_song_ids:
            playlist_song_ids_str += str(song_id[0]) + ","
        playlist_song_ids_str = "{}{}".format(playlist_song_ids_str[0: -1], ')')

        connect_db = sqlite3.connect('music_streaming_application.db')
        cursor = connect_db.cursor()

        query = 'SELECT \'' + playlist_name + '\', songs.song_name, songs.file_path, songs.singer, songs.song_release_date FROM songs WHERE song_id IN ' + playlist_song_ids_str
        #TODO: Seperate out playlist_name from the following command. Send it as a separate paameter. 
        cursor.execute(query)
        playlist_songs = cursor.fetchall()
        connect_db.close()

        return playlist_songs