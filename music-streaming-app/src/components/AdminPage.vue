<template>
    <div>
      <div class="d-flex flex-column flex-md-row align-items-center mb-4 border-bottom">
        <span class="ms-3 py-2 fs-4">Administrator Dashboard</span>
  
        <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
          <router-link to="/usermanagement" class="btn py-2 link-body-emphasis text-decoration-none btn-light me-3">User Management</router-link>
          <router-link to="/tracks" class="py-2 link-body-emphasis text-decoration-none btn btn-light me-3">Tracks</router-link>
          <button @click="logout()" class="me-3 py-2 link-body-emphasis text-decoration-none btn btn-outline-primary">Logout</button>
        </nav>
      </div>
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-3 text-center">
            <div class="card mb-3" style="height: 19rem;">
              <div class="card-body">
                <h3 class="card-title">Normal User</h3><br><br>
                <h1 style="font-size: 70px;">{{ total_users }}</h1>
              </div>
            </div>
  
            <div class="card text-center" style="height: 19rem;">
              <div class="card-body">
                <h3 class="card-title">Creator</h3><br><br>
                <h1 style="font-size: 70px;">{{ total_creators }}</h1>
              </div>
            </div>
          </div>
  
          <div class="col-md-9">
            <div class="row mb-3">
              <div class="col">
                <h3>App Performance</h3>
              </div>
            </div>
  
            <div class="row mb-3">
              <div class="col-md-4">
                <div class="card text-center" style="height: 11rem;">
                  <div class="card-body">
                    <h3 class="card-title">Tracks</h3><br>
                    <h1>{{ total_songs }}</h1>
                  </div>
                </div>
              </div>
  
              <div class="col-md-4">
                <div class="card text-center" style="height: 11rem;">
                  <div class="card-body">
                    <h3 class="card-title">Total Albums</h3><br>
                    <h1>{{ total_albums }}</h1>
                  </div>
                </div>
              </div>
  
              <div class="col-md-4">
                <div class="card text-center" style="height: 11rem;">
                  <div class="card-body">
                    <h3 class="card-title">Genre</h3><br>
                    <h1>{{ total_genres }}</h1>
                  </div>
                </div>
              </div>
            </div>
  
            <div class="row">
              <div class="col">
                <div class="card" style="height: 25rem;">
                  <div class="card-body">
                    <h3 class="card-title">Graphs</h3>
                    <canvas ref="chart" width="1050" height="330"></canvas>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script>
import Chart from 'chart.js/auto';
import axios from 'axios';
  
export default {
    data() {
      return {
        total_songs: 0,
        total_albums: 0,
        total_genres: 0,
        total_users: 0,
        total_creators: 0,
        labels: [],
        values: [],
      };
    },

    methods:{
        async getData(){
          // Fetch username and access token from Local Storage
            const username = localStorage.getItem('user'); // Fetch username from Local Storage
            const access_token = localStorage.getItem('access_token');
            if (!username) {
                console.error('Username not found in Local Storage');
                return;
            }

            const path = 'http://127.0.0.1:5000/admin'; // Include username in the request URL
            try {
              // Send a GET request to the server with the access token in the headers
                const res = await axios.get(path, {
                    headers: {
                        Authorization: `Bearer ${access_token}`
                    }
                });
                this.total_songs = res.data.total_songs;
                this.total_albums = res.data.total_albums;
                this.total_genres = res.data.total_genres;
                this.total_creators = res.data.total_creators;
                this.total_users = res.data.total_users;
                this.labels = res.data.labels;
                this.values = res.data.values;

                // Create a new Chart using Chart.js with the fetched data
                const ctx = this.$refs.chart.getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: this.labels,
                        datasets: [{
                            label: 'Data points',
                            data: this.values,
                        }],
                    },
                    options: {
                        responsive: false,
                    },
                });
            }
            catch (err) {
                console.error(err);
            }
        },

        async logout(){
          // Send a POST request to the server to logout the user
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
              // Remove access token and other user-related data from Local Storag
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
      // Call getData() when the component is mounted to fetch initial data
        this.getData();
    },
};
</script>
  
<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
</style>
  