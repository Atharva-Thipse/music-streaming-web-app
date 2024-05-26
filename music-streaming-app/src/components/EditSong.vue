<template>
    <div>
      <div class="d-flex flex-column flex-md-row align-items-center mb-4 border-bottom">
        <router-link to="/home" class="d-flex align-items-center link-body-emphasis text-decoration-none">
          <span class="ms-3 py-2 fs-4">Music Streaming App</span>
        </router-link>
  
        <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
            <router-link to="/upload" class="me-3 py-3 link-body-emphasis text-decoration-none">Upload Song</router-link>
            <router-link to="/home" class="me-3 py-3 link-body-emphasis text-decoration-none">User Account</router-link>
        </nav>
  
        <button @click="logout()" class="me-3 py-2 link-body-emphasis text-decoration-none btn btn-outline-primary">Logout</button>
      </div>
  
      <div class="row">
        <h1 align="center"><font size="+5">Edit Song</font></h1>
        <br><br><br>
      </div>
  
      <div class="row">
        <form class="form" @submit.prevent="editSong" enctype="multipart/form-data">
          <div class="d-grid col-7 justify-content-md-end">
            <h3>Title</h3>
            <input v-model="title" type="text" class="form-control" size="30" name="song_name" required>
          </div>
  
          <div class="d-grid col-7 justify-content-md-end">
            <br>
            <h3>Artist</h3>
            <input v-model="artist" type="text" class="form-control" size="30" name="song_singer" required>
          </div>
  
          <div class="d-grid col-7 justify-content-md-end">
            <br>
            <h3>Genre</h3>
            <input v-model="genre" type="text" class="form-control" size="30" name="song_genre">
          </div>
  
          <div class="d-grid col-7 justify-content-md-end">
            <br>
            <h3>Release Date</h3>
            <input v-model="releaseDate" type="date" class="form-control" style="width: 280px;" name="release_date" required>
          </div>
  
          <div class="d-grid col-7 justify-content-md-end m-1">
            <br>
            <h3>Lyrics</h3>
            <textarea v-model="lyrics" class="form-control" size="30" name="lyrics" rows="3" cols="33"></textarea>
          </div>
  
          <div class="text-center p-5">
            <button type="submit" class="btn btn-success" value="Upload" style="width: 150px;">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
<script>
import axios from 'axios';

export default {
    data() {
      return {
        title: '',
        artist: '',
        genre: '',
        releaseDate: '',
        lyrics: ''
      };
    },

    methods: {
      async editSong() {
        const access_token = localStorage.getItem('access_token');
        if (!access_token) {
            console.error('Access token not found in Local Storage');
            return;
        }

        try {
          // Send a request to edit the song details
            await axios.post(`http://127.0.0.1:5000/edit_song/${this.$route.params.song_id}`, {
                song_name: this.title,
                lyrics: this.lyrics,
                song_genre: this.genre,
                song_singer: this.artist,
                release_date: this.releaseDate
            }, {
                headers: {
                    Authorization: `Bearer ${access_token}`
                }
            });

            console.log('Song edited successfully');
            this.$router.push("/creator");
        } catch (error) {
            console.error('Failed to edit song:', error);
        }
    },

    async getSongDetails() {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found in Local Storage');
        return;
      }

      try {
        // Fetch the details of the song
        const response = await axios.get(`http://127.0.0.1:5000/edit_song/${this.$route.params.song_id}`, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        });

        const song = response.data.song;
        this.title = song[1];
        this.artist = song[5];
        this.genre = song[4];
        this.releaseDate = song[6];
        this.lyrics = song[3];
      } catch (error) {
        console.error('Failed to fetch song details:', error);
      }
    },

    logout(){
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found in Local Storage');
        return;
      }
      // Send a request to logout the user
      axios.post('http://127.0.0.1:5000/logout_user', null, {
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
    this.getSongDetails();
  }
};
</script>
  
<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
</style>
  