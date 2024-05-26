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

      <div class="row">
        <div class="col-6">
          <h3 class="ms-3">{{ album_name }}</h3>
        </div>
      </div>

    <br>

    <div class="card ms-3" style="width: 1400px; height: 500px;">
      <div v-for="song in albums" :key="song[0]">
        <div class="row card m-2" style="height: 49px;">
          <div class="col-md-6 d-flex">
                  <div>
                      <h5 class="mt-2">{{ song.song_name }}</h5>
                  </div>
                  <div>
                      <p class="mt-3 ms-2" style="font-size: 14px;">{{ song.singer }} | {{ song.song_release_date }}</p>
                  </div>
                </div>
                  <div class="col-md-6 d-flex justify-content-end mt-1 p-0">
                      <button style="width: 200px;" class="btn btn-info text-center me-2" type="submit"><router-link class="text-decoration-none text-dark" :to="'/song/' + song.song_name">View Details</router-link></button>
                      <audio name="audioPlayer" controls style="height: 40px; width: 1000px;">
                          <source :src="`http://127.0.0.1:5000/${song.file_path}`" type="audio/mpeg">
                          <source :src="`http://127.0.0.1:5000/${song.file_path}`" type="audio/ogg">
                          Your browser does not support the audio element.
                      </audio>
                  </div>
        </div>
      </div>
    </div>

    <div class="input-group-append text-center mt-3">
      <button class="py-2 link-body-emphasis text-decoration-none btn btn-outline-success" @click="playAllTracks">Play all tracks</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      albums: null,
      album_name: '',
      user_type: '',
      blacklisted: '',
      songIdx: 0,
    };
  },
  methods: {
    // Fetches data for the component from the backend
      async getData(){
          const username = localStorage.getItem('user'); // Fetch username from Local Storage
          const access_token = localStorage.getItem('access_token');
          if (!username) {
              console.error('Username not found in Local Storage');
              return;
          }

          const path = `http://127.0.0.1:5000/album/${this.$route.params.album_id}`;
          try {
              const res = await axios.get(path, {
                  headers: {
                      Authorization: `Bearer ${access_token}`
                  }
              });
              this.user_type = res.data.user_type;
              this.blacklisted = res.data.blacklisted;
              this.albums = res.data.songs;
              this.album_name = res.data.album_name;
          } catch (err) {
              console.error(err);
          }
      },

      // Registers the user as a creator
      register_as_creator(){
          const access_token = localStorage.getItem('access_token');
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

      playAllTracks(){
          this.playCurrentTrack(0);
      },

      playCurrentTrack(){
          const audioPlayers = document.getElementsByName('audioPlayer');

          audioPlayers[this.songIdx].addEventListener('ended', () => {
              console.log('ending song ' + this.songIdx);
              this.songIdx++;
              if (this.songIdx < audioPlayers.length) {
                  console.log('starting song ' + this.songIdx);
                  this.playCurrentTrack(this.songIdx);
              }
          })

          audioPlayers[this.songIdx].play();
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

      // Load Bootstrap JS script dynamically
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js';
      script.integrity = 'sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL';
      script.crossOrigin = 'anonymous';
      document.body.appendChild(script);
  },
};
</script>

<style>
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
