<template>
  <div class="d-flex flex-column flex-md-row align-items-center mb-4 border-bottom">
        <router-link to="/home" class="d-flex align-items-center link-body-emphasis text-decoration-none">
          <span class="ms-3 py-2 fs-4">Music Streaming App</span>
        </router-link>
  
        <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
            <form class="me-3 py-2 link-body-emphasis text-decoration-none" @submit.prevent="search" method="get">
                <div class="input-group">
                    <input v-model="searchText" class="py-2 link-body-emphasis text-decoration-none form-control" name="search" type="search" placeholder="Search" aria-label="Search" size="30" aria-describedby="basic-addon2">
                    <div class="input-group-append">
                        <button class="py-2 link-body-emphasis text-decoration-none btn btn-outline-success" type="submit">Search</button>
                    </div>
                </div>
            </form>
            
            <div class="modal fade" id="register_as_creator" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                  <div class="modal-header">
                    <h3 class="modal-title" id="exampleModalLabel">Register as Creator</h3>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>

                  <div class="modal-body">
                    Create new Songs, Albums and much more
                  </div>

                  <div class="modal-footer">
                    <form>
                      <button @click="register_as_creator()" type="submit" class="btn btn-success btn-lg btn-circle" data-bs-dismiss="modal" style="font-size: 20px;">+</button>
                    </form>
                  </div>
                </div>
              </div>
            </div>
            <router-link v-if="user_type === 'user'" to="/creator" class="me-3 py-3 link-body-emphasis text-decoration-none" data-bs-toggle="modal" data-bs-target="#register_as_creator">Creator Account</router-link>
            
            <router-link v-else-if="blacklisted === 0" class="me-3 py-3 link-body-emphasis text-decoration-none" to="/creator">Creator Account</router-link>
        </nav>

        <button @click="logout()" class="me-3 py-2 link-body-emphasis text-decoration-none btn btn-outline-primary">Logout</button>
    </div>

    <h4 class="ms-3">Songs</h4>
    <div class="card m-3" style="height: 10rem; overflow-x: auto;">
      <div class="d-flex flex-nowrap">
        <div v-for="song in songs" :key="song.song_id" class="card m-4" style="width: 13rem; height: 7rem; flex-shrink: 0;">
            <div class="card-body">
                <h5 class="card-title text-center">{{ song.song_name }}</h5>
                <div class="d-flex justify-content-center">
                  <button class="btn btn-info m-2">
                    <router-link class="text-decoration-none text-dark" :to="'/song/' + song.song_name">Lyrics</router-link>
                  </button>
                </div>
            </div>
        </div>
    </div>
          
    </div>

    <h4 class="ms-3">Albums</h4>

    <div class="card m-3" style="height: 10rem; overflow-x: auto;">
      <div class="d-flex flex-nowrap">
        <div v-for="album in albums" :key="album.album_id" class="card m-4" style="width: 13rem; height: 7rem; flex-shrink: 0;">
          <div class="card-body">
            <form class="form text-center" method="get" :action="'/album/' + album.album_id">
              <h5 class="card-title text-center">
                {{ album.album_name }}
              </h5>

              <button class="btn btn-info text-center m-2" type="submit"><a class="text-decoration-none text-dark" :href="'/album/' + album.album_id">View Tracks</a></button>
            </form>
          </div>
        </div>
      </div>
    </div>
    

    <div class="d-flex flex-column flex-md-row align-items-center mb-4">
      <h4 class="ms-3 me-auto">Your Playlist</h4>
      <button class="me-3 py-2 link-body-emphasis text-decoration-none btn btn-success text-light" @click="createPlaylist()">Create New Playlist</button>
    </div>
    <div class="card m-3" style="height: 10rem; overflow-x: auto;">
      <div class="d-flex flex-nowrap">
        <div v-for="playlist in playlists" :key="playlist.playlist_id" class="card m-4" style="width: 13rem; height: 7rem; flex-shrink: 0;">
          <div class="card-body">
            <form class="form text-center" method="get" :action="'/playlist/' + playlist.playlist_id">
              <h5 class="card-title text-center">
                {{ playlist.name }}
              </h5>

              <button class="btn btn-info text-center m-2" type="submit"><router-link class="text-decoration-none text-dark" :to="'/playlist/' + playlist.playlist_id">View Tracks</router-link></button>
            </form>
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
import axios from "axios";

export default {
  data() {
    return {
      user_type: null,
      blacklisted: null,
      songs: [],
      albums: [],
      playlists: [],
      searchText: '',
      searchResults: null,
    };
  },

  methods: {
    async getData() {
      const username = localStorage.getItem('user'); // Fetch username from Local Storage
      const access_token = localStorage.getItem('access_token');
      if (!username) {
        console.error('Username not found in Local Storage');
        return;
      }

      const path = 'http://127.0.0.1:5000/home_page'; // Include username in the request URL
      try {
        const res = await axios.get(path, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        });
        this.user_type = res.data.user_type;
        this.blacklisted = res.data.blacklisted;
        this.songs = res.data.songs;
        this.albums = res.data.albums;
        this.playlists = res.data.playlists;
      } catch (err) {
        console.error(err);
      }
    },

    register_as_creator(){
      const access_token = localStorage.getItem('access_token');
      localStorage.setItem('user_type', 'creator')
      if (!access_token) {
        console.error('Access token not found in Local Storage');
        return;
      }
      axios.post('http://127.0.0.1:5000/register_creator', null, {
        headers: {
          Authorization: `Bearer ${access_token}`
        }
      });
      this.$router.push("/creator");
    },

    search() {
      const access_token = localStorage.getItem('access_token');
      axios.get(`/searchadv?age=latest&searchIn=all&searchText=${this.searchText}&rating=0&mySongs=False&searchFor=null&count=10`, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        })
        .then(response => {
          this.searchResults = response.data;
          this.albums = response.data.albums;
          this.songs = response.data.songs;
          
          localStorage.setItem('searchFor', 'null');
          this.$router.push({ name: 'SongList', query: { searchResults: JSON.stringify(this.searchResults) } })
        })
        .catch(error => {
          console.error('Error searching:', error);
        });
    },

    createPlaylist() {
      localStorage.setItem('searchFor', 'create_playlist');
      const access_token = localStorage.getItem('access_token');
      axios.get(`/searchadv?age=latest&searchIn=song-name&searchText=&rating=0&mySongs=False&searchFor=create_playlist&count=10`, {
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

    async logout(){
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found in Local Storage');
        return;
      }

      await axios.post('http://127.0.0.1:5000/logout_user', null, {
        headers: {
          Authorization: `Bearer ${access_token}`
        }
      })
      .then(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        localStorage.removeItem('searchFor');
        localStorage.removeItem('user_type');
        this.$router.push("/");
      })
      .catch(error => {
        console.error('Logout failed:', error);
      });
    }
  },
  
  mounted() {
    this.getData(); // Fetch data when the component is mounted

    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js';
    script.integrity = 'sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL';
    script.crossOrigin = 'anonymous';
    document.body.appendChild(script);
  },
};
</script>
