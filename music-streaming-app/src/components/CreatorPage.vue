<template>
    <div>
      <div class="d-flex flex-column flex-md-row align-items-center mb-4 border-bottom">
        <router-link to="/home" class="d-flex align-items-center link-body-emphasis text-decoration-none">
          <span class="ms-3 py-2 fs-4">Music Streaming App</span>
        </router-link>
  
        <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
          <router-link to="/upload" class="me-3 py-3 link-body-emphasis text-decoration-none">Upload Song</router-link>
          <button class="btn me-3 py-3 link-body-emphasis text-decoration-none" @click="createAlbum()">Upload Album</button>
          <router-link to="/home" class="me-3 py-3 link-body-emphasis text-decoration-none">User Account</router-link>
        </nav>
        <button @click="logout()" class="me-3 py-2 link-body-emphasis text-decoration-none btn btn-outline-primary">Logout</button>
      </div>
  
      <div class="card m-3" style="height: 19rem;">
        <h1 class="m-3">Dashboard</h1>
        <div class="d-flex flex-nowrap">
          <div class="card m-4 ms-auto" style="width: 19rem; height: 11rem;">
            <div class="card-body" align="center">
              <h5>Total Songs Uploaded</h5><br>
              <h1>{{ total_songs }}</h1>
            </div>
          </div>
          <div class="card m-4 mx-auto" style="width: 19rem; height: 11rem;">
            <div class="card-body" align="center">
              <h5>Average Rating</h5><br>
              <h1>{{ average_rating }}</h1>
            </div>
          </div>
          <div class="card m-4 me-auto" style="width: 19rem; height: 11rem;">
            <div class="card-body" align="center">
              <h5>Total Albums</h5><br>
              <h1>{{ total_albums }}</h1>
            </div>
          </div>
        </div>
      </div>
      <div class="card m-3" style="height: 19rem; overflow-y: auto;">
        <div class="row m-3">
          <div class="col-6">
            <h1>Your Songs</h1>
          </div>
          <div class="col-6 text-end mt-2">
            <router-link to="/upload"><button class="btn btn-secondary">Upload Song</button></router-link>
          </div>
        </div>
  
        <div v-for="song in songs" :key="song.song_id" class="row card m-2" style="height: 49px;">
          <div class="col-md-6 d-flex">
            <div>
              <h5 class="mt-2">{{ song.song_name }}</h5>
            </div>
            <div>
              <p class="mt-3 ms-2" style="font-size: 14px;">{{ song.singer }} | {{ song.song_release_date }}</p>
            </div>
          </div>
          <div class="col-md-6 d-flex justify-content-end mt-1 p-0">
            <router-link :to="'/song/' + song.song_name" class="text-decoration-none text-dark"><button style="width: 200px;" class="btn btn-info text-center me-2" type="submit">View Details</button></router-link>
            <router-link :to="'/edit_song/' + song.song_id" class="text-decoration-none text-dark"><button style="width: 200px;" class="btn btn-warning text-center me-2" type="submit">Edit</button></router-link>
            <button style="width: 200px;" class="btn btn-danger text-center me-2 text-decoration-none text-dark" type="submit" @click="deleteSong(song.song_id)">Delete</button>
          </div>
        </div>
      </div>
      <div class="card m-3" style="height: 19rem; overflow-y: auto;">
        <div class="row m-3">
          <div class="col-6">
            <h1>Your Albums</h1>
          </div>
          <div class="col-6 text-end mt-2">
            <button class="btn btn-secondary" @click="createAlbum()">Upload Album</button>
          </div>
        </div>
  
        <div v-for="album in albums" :key="album.album_id" class="row card m-2" style="height: 49px;">
          <div class="col-md-6 d-flex">
            <div>
              <h5 class="mt-2">{{ album.album_name }}</h5>
            </div>
          </div>
          <div class="col-md-6 d-flex justify-content-end mt-1 p-0">
            <router-link :to="'/album/' + album.album_id" class="text-decoration-none text-dark"><button style="width: 200px;" class="btn btn-info text-center me-2" type="submit">View Details</button></router-link>
            <button style="width: 200px;" class="btn btn-warning text-center me-2 text-decoration-none text-dark" type="submit" @click="updateAlbum(album.album_id)">Edit</button>
            <button style="width: 200px;" class="btn btn-danger text-center me-2 text-decoration-none text-dark" type="submit" @click="deleteAlbum(album.album_id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
    
</template>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
::-webkit-scrollbar{
    display: none;
}

.navbar {
    justify-content: space-between;
}

.btn-circle { 
    width: 70px; 
    height: 70px; 
    padding: 10px 16px; 
    border-radius: 35px; 
    font-size: 12px; 
    text-align: center; 
}
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      total_songs: 0,
      average_rating: 0,
      total_albums: 0,
      songs: [],
      albums: []
    };
  },

  methods: {
    // Fetches data about the creator
    async getData() {
      const username = localStorage.getItem('user'); // Fetch username from Local Storage
      const access_token = localStorage.getItem('access_token');
      if (!username) {
        console.error('Username not found in Local Storage');
        return;
      }

      const path = 'http://127.0.0.1:5000/creator'; // Include username in the request URL
      try {
        const res = await axios.get(path, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        });
        this.total_songs = res.data.total_songs;
        this.total_albums = res.data.total_albums;
        this.songs = res.data.songs;
        this.average_rating = res.data.average_rating;
        this.albums = res.data.albums;
      } catch (err) {
        console.error(err);
      }
    },

    // Redirects to the SongList component for creating a new album
    createAlbum() {
      localStorage.setItem('searchFor', 'upload_album');
      const access_token = localStorage.getItem('access_token');
      // Fetch data for creating a new album
      axios.get(`/searchadv?age=latest&searchIn=song-name&searchText=&searchFor=upload_album&rating=0&mySongs=true&count=10`, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        })
        .then(response => {
          this.searchResults = response.data;
          this.songs = response.data.songs;
          
          this.$router.push({ name: 'SongList', query: { searchResults: JSON.stringify(this.searchResults) } })
        })
        .catch(error => {
          console.error('Error searching:', error);
        });
    },

    // Redirects to the SongList component for updating an album
    updateAlbum(albumId) {
      localStorage.setItem('searchFor', 'update_album');
      localStorage.setItem('albumId', albumId)
      const access_token = localStorage.getItem('access_token');
      // Fetch data for updating the selected album
      axios.get(`/searchadv?age=latest&searchIn=song-name&searchText=&searchFor=update_album&rating=0&mySongs=true&count=10&albumId=${albumId}`, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        })
        .then(response => {
          this.searchResults = response.data;
          this.songs = response.data.songs;
          
          this.$router.push({ name: 'SongList', query: { searchResults: JSON.stringify(this.searchResults) } })
        })
        .catch(error => {
          console.error('Error searching:', error);
        });
    },

    // Deletes an item (song or album) by sending a request to the backend
    async deleteItem(id, endpoint, array, successMessage) {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found in Local Storage');
        return;
      }

      try {
        await axios.delete(`http://127.0.0.1:5000/${endpoint}/${id}`, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        });
        // Remove the deleted item from the array
        this[array] = this[array].filter(item => item.id !== id);
        console.log(successMessage);
      } catch (error) {
        console.error(`Failed to delete ${endpoint}:`, error);
      }
    },

    // Usage for deleting a song
    deleteSong(songId) {
      this.deleteItem(songId, 'delete_song', 'songs', 'Song deleted successfully');
    },

    // Usage for deleting an album
    deleteAlbum(albumId) {
      this.deleteItem(albumId, 'delete_album', 'albums', 'Album deleted successfully');
    },

    async logout(){
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found in Local Storage');
        return;
      }

      // Send a request to logout the user
      await axios.post('http://127.0.0.1:5000/logout_user', null, {
        headers: {
          Authorization: `Bearer ${access_token}`
        }
      })
      .then(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        localStorage.removeItem('user_type');
        localStorage.removeItem('searchFor');
        
        this.$router.push("/");
      })
      .catch(error => {
        console.error('Logout failed:', error);
      });
    }
  },

  mounted() {
    this.getData(); // Fetch data when the component is mounted
  },
};
</script>