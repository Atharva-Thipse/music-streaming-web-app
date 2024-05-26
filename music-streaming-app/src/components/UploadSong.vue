<template>
    <div>
      <div class="d-flex flex-column flex-md-row align-items-center mb-4 border-bottom">
        <router-link to="/home" class="d-flex align-items-center link-body-emphasis text-decoration-none">
          <span class="ms-3 py-2 fs-4">Music Streaming App</span>
        </router-link>
  
        <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
          <a class="me-3 py-3 link-body-emphasis text-decoration-none" href="#">Upload Song</a>
          <router-link to="/home" class="me-3 py-3 link-body-emphasis text-decoration-none">User Account</router-link>
        </nav>

        <button @click="logout()" class="me-3 py-2 link-body-emphasis text-decoration-none btn btn-outline-primary">Logout</button>
      </div>
  
      <div class="row">
        <h1 align="center"><font size="+5">Upload Song</font></h1>
        <br><br><br>
      </div>
  
      <div class="row">
        <form class="form" @submit.prevent="uploadSong" enctype="multipart/form-data">
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
            <input v-model="releaseDate" type="date" class="form-control" style="width: 280px;" name="release_date" pattern="\d{4}-\d{2}-\d{2}" required>
          </div>
  
          <div class="d-grid col-7 justify-content-md-end m-1">
            <br>
            <h3>Lyrics</h3>
            <textarea v-model="lyrics" class="form-control" size="30" name="lyrics" rows="3" cols="33"></textarea>
          </div>
  
          <div class="d-grid col-7 justify-content-md-end m-3">
            <br>
            <h3>Upload .mp3 File Here</h3>
            <input type="file" class="form-control-file" required name="song" @change="onFileChange">
          </div>
  
          <div class="text-center p-5">
            <button type="submit" class="btn btn-success btn-lg" value="Upload" style="width: 100px;">Upload</button>
          </div>
        </form>
      </div>
    </div>
</template>

<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      title: '',
      artist: '',
      genre: '',
      releaseDate: '',
      lyrics: '',
      file: null
    };
  },

  methods: {
    onFileChange(event) {
    this.file = event.target.files[0];
    },
    async uploadSong() {
      try {
        const formData = new FormData();
        formData.append('song', this.file);
        formData.append('title', this.title);
        formData.append('artist', this.artist);
        formData.append('genre', this.genre);
        formData.append('releaseDate', this.releaseDate);
        formData.append('lyrics', this.lyrics);

        const access_token = localStorage.getItem('access_token');
        if (!access_token) {
          console.error('Access token not found in Local Storage');
          return;
        }

        await axios.post('http://127.0.0.1:5000/upload_song', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${access_token}`
          }
        });

        this.$router.push("/creator");
      } catch (error) {
        console.error(error.message);
      }
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
  }
};
</script>