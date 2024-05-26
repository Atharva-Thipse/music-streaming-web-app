<template>
    <div>
      <div class="d-flex flex-column flex-md-row align-items-center mb-3 border-bottom">
        <span class="ms-3 py-2 fs-4">Administrator Dashboard</span>
        <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
          <router-link class="btn py-2 link-body-emphasis text-decoration-none btn-light me-3" to="/admin">Dashboard</router-link>
        </nav>
      </div>
      
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h1 class="ms-3">All Tracks</h1>
        <form @submit.prevent="searchTracks" class="me-3 py-2 link-body-emphasis text-decoration-none">
          <div class="input-group">
            <input v-model="searchText" class="py-2 link-body-emphasis text-decoration-none form-control" name="search" type="search" placeholder="Search Tracks" aria-label="Search" size="30" aria-describedby="basic-addon2">
            <div class="input-group-append">
              <button class="py-2 link-body-emphasis text-decoration-none btn btn-outline-success" type="submit">Search</button>
            </div>
          </div>
        </form>
      </div>
  
      <div v-for="(songs, genre) in songsByGenre" :key="genre" class="card m-3" style="height: 19rem; overflow: auto;">
        <h4 class="m-2">{{ genre }}</h4>
        <div v-for="song in songs" :key="song[0]" class="row card m-2" style="height: 49px;">
          <div class="col-md-6 d-flex">
            <div>
              <h5 class="mt-2">
                <a class="text-decoration-none text-dark song-name" href="#" :data-audio-src="`{{ url_for('static', filename='audio/' + song[2].split('\\')[-1]) }}`">{{ song[1] }}</a>
              </h5>
            </div>
            <div>
              <p class="mt-3 ms-2" style="font-size: 14px;">{{ song[5] }} | {{ song[6] }}</p>
            </div>
          </div>
          <div class="col-md-6 d-flex justify-content-end mt-1 p-0">
            <router-link :to="'/song/' + song[1]" class="text-decoration-none text-dark"><button style="width: 200px;" class="btn btn-info text-center me-2" type="submit">View Details</button></router-link>
            <button style="width: 200px;" class="btn btn-danger text-center me-2 text-decoration-none text-dark" type="submit" @click="deleteSong(song[0])">Delete</button>
          </div>
        </div>
      </div>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
    data() {
      return {
        songsByGenre: {},
        searchFor: '',
        searchText: '',
      };
    },
    methods: {
      fetchTracks() {
        const access_token = localStorage.getItem('access_token');
        axios.get('http://127.0.0.1:5000/tracks', {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        })
          .then(response => {
            this.songsByGenre = response.data.songs_by_genre;
            this.searchFor = response.data.searchFor;

            localStorage.setItem('searchFor', response.data.searchFor);
          })
          .catch(error => {
            console.error('Error fetching tracks:', error);
          });
      },
      searchTracks() {
        // Handle search functionality based on this.searchFor
        const access_token = localStorage.getItem('access_token');
        this.searchFor = localStorage.getItem('searchFor');
        axios.get(`/searchadv?age=latest&searchIn=all&searchText=${this.searchText}&rating=0&mySongs=False&searchFor=${this.searchFor}&count=10`, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        })
        .then(response => {
          this.searchResults = response.data;
          this.albums = response.data.albums;
          this.songs = response.data.songs;
          
          localStorage.setItem('searchFor', 'tracks_record');
          this.$router.push({ name: 'SongList', query: { searchResults: JSON.stringify(this.searchResults) } })
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
            // Remove the deleted song from the songsByGenre object
            for (let genre in this.songsByGenre) {
                this.songsByGenre[genre] = this.songsByGenre[genre].filter(song => song[0] !== songId);
            }
            console.log('Song deleted successfully');
        } catch (error) {
            console.error('Failed to delete song:', error);
        }
      },
    },
    mounted() {
      this.fetchTracks();
    },
};
</script>

<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
::-webkit-scrollbar{
    display: none;
}
</style>
  