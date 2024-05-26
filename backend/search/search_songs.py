import sqlite3

#Get text search condition for a column based on whether to match from start or anywhere
def get_search_cnd (column_name: str, text: str, fromStart: bool):
    if (fromStart):
        cnd_str = column_name + " LIKE " + "\'" + text + "%\'"
    else:
        cnd_str =  column_name + " LIKE "     + "\'%" + text + "%\' and "
        cnd_str += column_name + " not LIKE " + "\'" + text + "%\'"
    return cnd_str

# Return a comma-seperated string having album ids matching the text in album name.
# Example: "1, 5, 8,..." 
def get_album_ids_for_name_search(text: str, fromStart: bool):
    if (fromStart):
        cnd_str = "album_name LIKE " + "\'" + text + "%\'"
    else:
        cnd_str =  "album_name  LIKE "     + "\'%" + text + "%\' and "
        cnd_str += "album_name  not LIKE " + "\'" + text + "%\'"

    # We are already connected to this database, but we need to do it again just to get the cursor
    # TODO: A better approach will be to a class containing cursor and all these functions
    connect_db = sqlite3.connect('music_streaming_application.db')
    cursor = connect_db.cursor()

    cursor.execute('SELECT album_id FROM album WHERE ' + cnd_str)
    album_ids = cursor.fetchall()

    connect_db.close()

    album_ids_str = ""
    for album_id in album_ids:
        album_ids_str += str(album_id[0]) + ","
    album_ids_str = album_ids_str[:-1]

    return album_ids_str

#Get the where clause for getting songs list as per the search text
def get_where_clause_for_song_search (text: str, searchIn: str, fromStart: bool, rating: int, user: str):
    where_clause = ""

    if (len(text)):
        if (searchIn == "song-name" or searchIn == "all"):
            if (len(where_clause) > 0):
                where_clause += " or "
            where_clause += get_search_cnd ("song_name", text, fromStart)
        elif (searchIn == "lyrics" or searchIn == "all"):
            if (len(where_clause) > 0):
                where_clause += " or "
            where_clause += get_search_cnd ("lyrics", text, fromStart)
        elif (searchIn == "artist" or searchIn == "all"):
            if (len(where_clause) > 0):
                where_clause += " or "
            where_clause += get_search_cnd ("singer", text, fromStart)
        elif (searchIn == "genre" or searchIn == "all"):
            if (len(where_clause) > 0):
                where_clause += " or "
            where_clause += get_search_cnd ("genre", text, fromStart)
        elif (searchIn == "album-name" or searchIn == "all"):
    # Get all albums matching the query
            album_ids_str = get_album_ids_for_name_search(text, fromStart)
            if album_ids_str:
                if (len(where_clause) > 0):
                    where_clause += " or "
                where_clause += "album_id IN (" + album_ids_str + ")"

    
    if (rating > 0):
        if (len(where_clause) > 0):
            where_clause += " and "
        where_clause += "avg_rating >= " + str(rating)

    if (len(user) > 0):
        if (len(where_clause) > 0):
            where_clause += " and "
        where_clause += "owner = \'" + user + '\''

    return where_clause

# Function to get songs based on search criteria
def get_search_songs(cursor, text: str, searchIn: str, fromStart: bool, rating: int, user: str, count: int, age: str):
    whereClause = get_where_clause_for_song_search(text, searchIn, fromStart, rating, user)
    query = "SELECT * FROM songs"

    if len(whereClause) > 0:
        query += " WHERE " + whereClause

    if searchIn == "album-name" and not whereClause:
        # If searching only by album name and no other conditions, return only albums
        album_ids_str = get_album_ids_for_name_search(text, fromStart)
        if album_ids_str:
            query = "SELECT * FROM album WHERE album_id IN (" + album_ids_str + ")"
            cursor.execute(query)

            albums = cursor.fetchmany(count)
            return albums
        else:
            # If no albums found, return an empty list
            return []

    elif age == "latest" and not searchIn == "album-name":
        query += " ORDER BY song_release_date DESC"

    cursor.execute(query)

    songs = cursor.fetchmany(count)
    return songs