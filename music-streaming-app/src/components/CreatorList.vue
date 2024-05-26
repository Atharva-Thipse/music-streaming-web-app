<template>
    <div>
      <div class="d-flex flex-column flex-md-row align-items-center mb-4 border-bottom">
        <span class="ms-3 py-2 fs-4">Administrator Dashboard</span>
        <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
          <router-link class="btn py-2 link-body-emphasis text-decoration-none btn-light me-3" to="/admin">Dashboard</router-link>
        </nav>
      </div>
  
      <div v-for="creator in creatorsList" :key="creator[0]" class="row card m-2" style="height: 49px;">
        <div class="col-md-6 d-flex">
          <div>
            <h4 class="mt-2">{{ creator[0] }}</h4>
          </div>
          <p class="mt-3 ms-2" style="font-size: 14px;">{{ creator[1] === 1 ? 'Blacklisted' : 'Whitelisted' }}</p>
        </div>
        <div class="col-md-6 d-flex justify-content-end mt-1 p-0">
          <form @submit.prevent="whitelistCreator(creator[0])">
            <button style="width: 150px;" class="btn btn-warning text-center me-3" type="submit" :disabled="creator[1] === 0">White List</button>
          </form>
          <form @submit.prevent="blacklistCreator(creator[0])">
            <button style="width: 150px;" class="btn btn-danger text-center me-2" type="submit" :disabled="creator[1] === 1">Black List</button>
          </form>
        </div>
      </div>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
    data() {
      return {
        creatorsList: [],
      };
    },

    methods: {
      // Fetches the list of creators from the backend
        fetchCreatorsList() {
            const username = localStorage.getItem('user'); // Fetch username from Local Storage
            const access_token = localStorage.getItem('access_token');
            if (!username) {
                console.error('Username not found in Local Storage');
                return;
            }

            axios.get('http://127.0.0.1:5000/usermanagement', {
                headers: {
                    Authorization: `Bearer ${access_token}`
                }
            })
              .then(response => {
                this.creatorsList = response.data.creators_list;
            })
            .catch(error => {
                console.error('Error fetching creators list:', error);
            });
        },

        whitelistCreator(username) {
            const access_token = localStorage.getItem('access_token');
            // Send a request to whitelist the creator
            axios.post('http://127.0.0.1:5000/whitelist_creator', { username }, {
                headers: {
                    Authorization: `Bearer ${access_token}`
                }
            })
            .then(() => {
              // Refresh the creators list after whitelisting
                this.fetchCreatorsList();
            })
            .catch(error => {
                console.error('Error whitelisting creator:', error);
            });
        },
        
        blacklistCreator(username) {
            const access_token = localStorage.getItem('access_token');
            // Send a request to blacklist the creator
            axios.post('http://127.0.0.1:5000/blacklist_creator', { username }, {
                headers: {
                    Authorization: `Bearer ${access_token}`
                }
            })
            .then(() => {
              // Refresh the creators list after blacklisting
                this.fetchCreatorsList();
            })
            .catch(error => {
                console.error('Error blacklisting creator:', error);
            });
        },
    },

    mounted() {
      // Fetch the creators list when the component is mounted
      this.fetchCreatorsList();
    },
};
</script>
  
<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
</style>
  