<template>
    <div class="d-flex flex-column flex-md-row align-items-center mb-4 border-bottom">
      <router-link to="/home" class="d-flex align-items-center link-body-emphasis text-decoration-none">
        <span class="ms-3 py-2 fs-4">Music Streaming App</span>
      </router-link>
      <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
        <form @submit.prevent="search" class="me-3 py-2 link-body-emphasis text-decoration-none" method="get">
          <div class="input-group">
            <label for="age" class="me-2 mt-2">Age:</label>
            <select v-model="age" id="age" name="age" class="me-2" style="height: 40px;">
              <option value="latest">Latest</option>
              <option value="all">All</option>
            </select>
            <label for="searchIn" class="me-2 mt-2">Search In:</label>
            <select v-model="searchIn" class="me-2" style="height: 40px;">
              <option v-for="option in searchOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
            </select>
            <input v-model="searchText" class="py-2 link-body-emphasis text-decoration-none form-control me-2" name="searchText" type="search" placeholder="Search" aria-label="Search" size="30" aria-describedby="basic-addon2">
            <label for="rating" class="me-2 mt-2">Rating:</label>
            <select v-model="selectedRating" id="rating" name="rating" class="me-2" style="height: 40px; width: 40px;">
              <option v-for="option in ratingOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
            </select>
            <label class="me-2 mt-2">My songs:</label>
            <div class="form-check mt-2">
              <input type="checkbox" class="form-check-input me-2" id="mySongsCheckbox" style="height: 20px; width: 20px;" v-model="mySongs" :disabled="searchFor === 'upload_album' || searchFor === 'update_album'" :checked="searchFor === 'upload_album' || searchFor === 'update_album'">
              <input type="hidden" name="mySongs" :value="mySongs">
              <input type="hidden" name="searchFor" :value="searchFor">
            </div>
            <label for="count" class="me-2 mt-2">Count:</label>
            <select v-model="count" id="count" name="count" class="me-2" style="height: 40px;">
              <option v-for="option in countOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
            </select>
            <div class="input-group-append">
              <button class="py-2 link-body-emphasis text-decoration-none btn btn-outline-success" type="submit">Search</button>
            </div>
          </div>
        </form>
      </nav>
    </div>
    
    <!-- Display search results -->
    <div v-if="searchFor === 'upload_album'" style="overflow: auto;">
    <form @submit.prevent="createAlbum" id="newAlbumForm" method="post">
      <div class="card ms-3" style="width: 1450px; height: 580px">
        <div v-for="song in songs" :key="song[0]" class="row card m-2" style="height: 49px; width: 1430px;">
          <h5 class="mt-2">
            {{ song[1] }}
            <div class="float-end">
              <div class="form-check">
                <input type="checkbox" class="form-check-input" name="check_song" :value="song[0]" v-model="selectedSongIds">
              </div>
            </div>
          </h5>
        </div>
      </div>

      <div class="modal fade" id="new_album" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h3 class="modal-title" id="exampleModalLongTitle">Create New Album</h3>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <input v-model="album_name" type="text" class="form-control" name="album_name" placeholder="Enter Album Name" required>
            </div>
            <div class="modal-footer">
              <button data-bs-dismiss="modal" type="submit" class="btn btn-success" name="new_album">Create Album</button>
            </div>
          </div>
        </div>
      </div>
    </form>
    </div>

    <div v-else-if="searchFor === 'update_album'" style="overflow: auto;">
      <div class="card ms-3" style="width: 1450px; height: 580px">
        <div v-for="song in songs_in_album" :key="song[0]" class="row card m-2" style="height: 49px; width: 1430px;">
          <h5 class="mt-2">
            {{ song[1] }}
            <div class="float-end">
              <div class="form-check">
                <input type="checkbox" class="form-check-input" name="check_song" :value="song[0]" :checked="true" v-model="selectedSongIds">
              </div>
            </div>
          </h5>
        </div>

        <div v-for="song in songs_not_in_album" :key="song[0]" class="row card m-2" style="height: 49px; width: 1430px;">
          <h5 class="mt-2">
            {{ song[1] }}
            <div class="float-end">
              <div class="form-check">
                <input type="checkbox" class="form-check-input" name="check_song" :value="song[0]" v-model="selectedSongIds">
              </div>
            </div>
          </h5>
        </div>
      </div>
    </div>

    <div v-else-if="searchFor === 'tracks_record'" class="card ms-3" style="width: 1450px; height: 580px; overflow: auto;">
      <div v-for="song in songs" :key="song[0]" class="row card m-2" style="height: 49px;">
        <div class="col-md-6 d-flex">
          <div>
            <h5 class="mt-2">{{ song[1] }}</h5>
          </div>
          <div>
            <p class="mt-3 ms-2" style="font-size: 14px;">{{ song[5] }} | {{ song[6] }}</p>
          </div>
        </div>
        <div class="col-md-6 d-flex justify-content-end mt-1 p-0">
          <a :href="`/song/${song[1]}`" class="text-decoration-none text-dark"><button style="width: 200px;" class="btn btn-info text-center me-2" type="submit">View Lyrics</button></a>
          <a :href="`/delete_song/${song[0]}`" class="text-decoration-none text-dark"><button style="width: 200px;" class="btn btn-danger text-center me-2" type="submit">Delete</button></a>
        </div>
      </div>
    </div>
    <div v-else class="d-flex flex-nowrap">
      <form v-if="searchIn" class="form" id="addTracksForm" @submit.prevent="createPlaylist" method="post">
        <div class="card ms-3" style="width: 1450px; height: 580px">
          <div v-if="searchIn === 'album-name'">
            <div v-for="album in albums" :key="album[0]" class="row card m-2" style="height: 50px; width: 1430px;">
              <div class="col-md-6">
                <h5 class="mt-2">{{ album[1] }}</h5>
              </div>
              <div class="col-md-6">
                <div class="float-end mt-1">
                  <button class="btn btn-info" type="submit">
                    <a class="text-decoration-none text-dark" :href="'/album/' + album[0]">View Tracks</a>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div v-else-if="searchIn === 'all'">
            <div v-for="song in songs" :key="song[0]" class="row card m-2" style="height: 49px; width: 1430px;">
              <h5 class="mt-2">
                {{ song[1] }}
                <div class="float-end">
                  <div class="form-check">
                    <input type="checkbox" class="form-check-input" name="check_song" :value="song[0]" v-model="selectedSongIds">
                  </div>
                </div>
              </h5>
            </div>
            <div v-for="album in albums" :key="album[0]" class="row card m-2" style="height: 50px; width: 1430px;">
              <div class="col-md-6">
                <h5 class="mt-2">{{ album[1] }}</h5>
              </div>
              <div class="col-md-6">
                <div class="float-end mt-1">
                  <button class="btn btn-info" type="submit">
                    <a class="text-decoration-none text-dark" :href="'/album/' + album[0]">View Tracks</a>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <div v-for="song in songs" :key="song[0]" class="row card m-2" style="height: 49px; width: 1430px;">
              <h5 class="mt-2">
                {{ song[1] }}
                <div class="float-end">
                  <div class="form-check">
                    <input type="checkbox" class="form-check-input" name="check_song" :value="song[0]" v-model="selectedSongIds">
                  </div>
                </div>
              </h5>
            </div>
          </div>
        </div>

        <!-- Modal form for adding to existing playlist -->
        <div class="modal fade" id="update_playlist" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h3 class="modal-title" id="exampleModalLongTitle">Update Playlist</h3>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <div v-for="playlist in playlists" :key="playlist[0]" class="row">
                  <h5>{{ playlist[1] }}
                    <div class="float-end">
                      <div class="form-check">
                        <input type="checkbox" class="form-check-input" name="check_playlist" :value="playlist[0]" v-model="selectedPlaylistsIds">
                      </div>
                    </div>
                  </h5>
                </div>
              </div>
              <div class="modal-footer">
                <button type="submit" data-bs-dismiss="modal" class="btn btn-success" name="update_playlist" @click="onAddTracksToExisingPlaylists()">Update Playlist</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal form for creating new playlist -->
        <div class="modal fade" id="new_playlist" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h3 class="modal-title" id="exampleModalLongTitle">Create New Playlist</h3>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <input type="text" class="form-control" v-model="playlist_name" placeholder="Enter Playlist Name" required>
              </div>
              <div class="modal-footer">
                <button type="submit" class="btn btn-success" data-bs-dismiss="modal" name="new_playlist">Create Playlist</button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>

    <div v-if="searchFor === 'create_playlist'" class="row">
      <div class="text-center">
        <button type="button" class="btn btn-success mt-3" data-bs-toggle="modal" data-bs-target="#new_playlist">Create Playlist</button>
      </div>
    </div>
    <div v-else-if="searchFor === 'upload_album'" class="row">
      <div class="text-center">
        <button type="button" class="btn btn-success mt-3" data-bs-toggle="modal" data-bs-target="#new_album">Upload Album</button>
      </div>
    </div>
    <div v-else-if="searchFor === 'update_album'" class="row">
      <div class="text-center">
        <button type="button" class="btn btn-primary mt-3" @click="updateAlbum()">Update Album</button>
      </div>
    </div>
    <div v-else-if="searchFor === 'tracks_record'" class="row"></div>
    <div v-else class="row">
      <div class="d-grid gap-2 col-5 justify-content-md-end">
        <button type="button" class="btn btn-success mt-3" data-bs-toggle="modal" data-bs-target="#new_playlist">Create Playlist</button>
      </div>
      <div class="d-grid gap-2 col-3 justify-content-md-end">
        <button type="button" class="btn btn-primary mt-3" data-bs-toggle="modal" data-bs-target="#update_playlist">Update Playlist</button>
      </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      songs: [],
      songs_not_in_album: [],
      songs_in_album: [],
      albums: [],
      playlists: [],
      mySongs: false,
      age: 'latest',
      searchText: '',
      selectedRating: 0, // Add rating property
      count: 10, // Default count value
      searchResults: null,
      searchFor: '',
      searchIn: 'all',
      searchOptions: [
        { label: 'Album name', value: 'album-name' },
        { label: 'Song name', value: 'song-name' },
        { label: 'Lyrics', value: 'lyrics' },
        { label: 'Artist', value: 'artist' },
        { label: 'Genre', value: 'genre' },
        { label: 'All', value: 'all' },
      ],
      ratingOptions: [
        { value: 0, label: 'All' },
        { value: 1, label: '1' },
        { value: 2, label: '2' },
        { value: 3, label: '3' },
        { value: 4, label: '4' },
        { value: 5, label: '5' },
      ],
      countOptions: [
        { value: 10, label: '10' },
        { value: 25, label: '25' },
        { value: 50, label: '50' },
        { value: 100, label: '100' },
      ],
      playlist_name: '',
      selectedSongIds: [],
      selectedPlaylistsIds: [],
      album_name: '',
    };
  },
  methods: {
    search() {
      const access_token = localStorage.getItem('access_token');
      this.searchFor = localStorage.getItem('searchFor');
      const albumId = localStorage.getItem('albumId');
      if (this.searchFor == 'upload_album' || this.searchFor === 'update_album'){
        this.mySongs = true;
      }
      axios.get(`/searchadv?age=${this.age}&searchIn=${this.searchIn}&searchText=${this.searchText}&rating=${this.selectedRating}&mySongs=${this.mySongs}&searchFor=${this.searchFor}&count=${this.count}&albumId=${albumId}`, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        })
        .then(response => {
          this.searchResults = response.data;
          this.albums = response.data.albums;
          this.songs = response.data.songs;
          this.playlists = response.data.playlists;
        })
        .catch(error => {
          console.error('Error searching:', error);
        });
    },
    async deleteSong(songId) {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found in Local Storage');
        return;
      }

      try {
        await axios.delete(`http://127.0.0.1:5000/delete_song/${songId}`, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        });
        // Remove the deleted song from the songs array
        this.songs = this.songs.filter(song => song.song_id !== songId);
        console.log('Song deleted successfully');
      } catch (error) {
        console.error('Failed to delete song:', error);
      }
    },
    onAddTracksToExisingPlaylists() {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found in Local Storage');
        return;
      }

      axios.post('http://127.0.0.1:5000/add_in_playlist', {
        playlist_name: this.playlist_name,
        check_song: this.selectedSongIds,
        check_playlist: this.selectedPlaylistsIds,
      }, {
        headers: {
          Authorization: `Bearer ${access_token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        console.log('Playlist created successfully', response);
      })
      .catch(error => {
        console.error('Error creating playlist:', error);
      });
    },
    async createPlaylist() {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found in Local Storage');
        return;
      }

      try {
        const res = await axios.post('http://127.0.0.1:5000/add_in_playlist', {
          playlist_name: this.playlist_name,
          check_song: this.selectedSongIds,
          check_playlist: this.selectedPlaylistsIds,
        }, {
          headers: {
            Authorization: `Bearer ${access_token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log('Playlist created successfully', res);
      } catch (err) {
        console.error('Error creating playlist:', err);
      }
    },
    async createAlbum() {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found in Local Storage');
        return;
      }

      try {
        const res = await axios.post('http://127.0.0.1:5000/add_in_album', {
          album_name: this.album_name,
          check_song: this.selectedSongIds,
        }, {
          headers: {
            Authorization: `Bearer ${access_token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log('Playlist created successfully', res);
      } catch (err) {
        console.error('Error creating playlist:', err);
      }
    },
    updateAlbum() {
      const access_token = localStorage.getItem('access_token');
      const albumId = localStorage.getItem('albumId');

      const newSongIds = this.selectedSongIds.filter(id => !this.songs_in_album.map(song => song[0]).includes(id));
      const oldSongIds = this.songs_in_album.map(song => song[0]).filter(id => !this.selectedSongIds.includes(id));

      axios.post(`/edit_album/${albumId}`, {
        new_songs_in_album: newSongIds,
        old_songs_in_album: oldSongIds,
      }, {
        headers: {
          Authorization: `Bearer ${access_token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        console.log('Album updated successfully', response);
        // Update the songs_in_album and songs_not_in_album based on the response
        localStorage.removeItem('albumId');
        localStorage.removeItem('searchFor');
        this.$router.push('/creator');
      })
      .catch(error => {
        console.error('Error updating album:', error);
      });
    },
  },
  mounted(){
    const searchResults = JSON.parse(this.$route.query.searchResults || null);
    if (searchResults) {
      this.searchResults = searchResults;
      this.searchFor = searchResults.searchFor;
      this.albums = searchResults.albums;
      this.playlists = searchResults.playlists;
      this.songs = searchResults.songs;
      this.songs_not_in_album = searchResults.songs_not_in_album;
      this.songs_in_album = searchResults.songs_in_album;
      this.searchIn = searchResults.searchIn;
    }

    this.selectedSongIds = this.songs_in_album.map(song => song[0]);
    
    // Disable checkbox interaction and update hidden field value on page load
    document.addEventListener("DOMContentLoaded", function() {
        const mySongsCheckbox = document.getElementById('mySongsCheckbox');
        const mySongsHidden = document.getElementById('mySongsHidden');

        if (mySongsCheckbox && mySongsHidden) {
          mySongsCheckbox.addEventListener('change', function() {
            mySongsHidden.value = this.checked;
          });
        }

        // Trigger the 'change' event to initialize the hidden field value
        mySongsCheckbox.dispatchEvent(new Event('change'));
    });

    document.addEventListener('DOMContentLoaded', function() {
      // Get the audio element and play button by their IDs
      var audioPlayer = document.getElementById('audio-player');

      // Get all the song name elements by their class
      var songNames = document.querySelectorAll('.song-name');

      // Add a click event listener to each song name element
      songNames.forEach(function(songName) {
        songName.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default link behavior

            // Get the audio source URL from the clicked song name element's data attribute
            var audioSource = songName.getAttribute('data-audio-src');

            // Set the audio player's source to the clicked song's source
            audioPlayer.src = audioSource;

            // Load the new audio source
            audioPlayer.load();

            // Play the audio
            if (audioPlayer.paused){
              audioPlayer.play();
            }else{
              audioPlayer.pause();
            }
        });
      });
    });

    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js';
    script.integrity = 'sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL';
    script.crossOrigin = 'anonymous';
    document.body.appendChild(script);
  }
};
</script>

<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
::-webkit-scrollbar{
    display: none;
}
</style>
