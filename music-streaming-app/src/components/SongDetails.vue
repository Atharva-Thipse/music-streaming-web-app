<template>
    <div>
      <div class="d-flex flex-column flex-md-row align-items-center mb-4 border-bottom">
        <router-link to="/home" class="d-flex align-items-center link-body-emphasis text-decoration-none">
          <span class="ms-3 py-2 fs-4">Music Streaming App</span>
        </router-link>
  
        <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
          <form @submit.prevent="search" class="me-3 py-2 link-body-emphasis text-decoration-none">
            <div class="input-group">
              <input v-model="searchText" class="py-2 link-body-emphasis text-decoration-none form-control" name="search" type="search" placeholder="Search" aria-label="Search" size="30" aria-describedby="basic-addon2">
              <div class="input-group-append">
                <button class="py-2 link-body-emphasis text-decoration-none btn btn-outline-success" type="submit">Search</button>
              </div>
            </div>
          </form>
  
          <router-link v-if="user_type === 'user'" to="/creator" class="me-3 py-3 link-body-emphasis text-decoration-none" data-bs-toggle="modal" data-bs-target="#register_as_creator">Creator Account</router-link>
  
          <a v-else-if="blacklisted === 0" href="/creator" class="me-3 py-3 link-body-emphasis text-decoration-none">Creator Account</a>
        </nav>
  
        <button @click="logout()" class="me-3 py-2 link-body-emphasis text-decoration-none btn btn-outline-primary">Logout</button>
      </div>
  
      <div v-if="song">
        <div class="card mx-auto" style="width: 50rem; height: 40rem;">
          <div class="d-flex flex-column flex-md-row align-items-center mt-3">
            <div class="card-title me-auto ms-3">
              <h3>{{ song[1] }} <span style="font-size: 15px;">{{ song[6] }}</span></h3>
            </div>
  
            <a class="me-3 py-2 link-body-emphasis text-decoration-none btn btn-warning" style="width: 100px;" href="#" data-bs-toggle="modal" data-bs-target="#rateModal">Rate</a>
          </div>
  
          <audio class="ms-2 mb-2" controls style="height: 40px;">
            <source :src="`http://127.0.0.1:5000/${song[2]}`" type="audio/mpeg">
            <source :src="`http://127.0.0.1:5000/${song[2]}`" type="audio/ogg">
            Your browser does not support the audio element.
          </audio>
  
          <h6 class="ms-3">{{ song[4] }} | {{ song[5] }}</h6>
  
          <div class="card mx-auto" style="width: 40rem; height: 29rem;">
            <pre class="ms-3 me-3">{{ song[3] }}</pre>
          </div>
  
          <a class="ms-3 mt-2 text-decoration-none text-dark" href="#" data-bs-toggle="modal" data-bs-target="#commentModal">Comment</a>
        </div>
      </div>
  
      <p v-else>Song not found</p>
  
      <div class="modal fade" id="register_as_creator" tabindex="-1" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h3 class="modal-title" id="exampleModalLongTitle">Register as Creator</h3>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
  
            <div class="modal-body">
              Create new Songs, Albums and much more
            </div>
  
            <div class="modal-footer">
              <form method="post" action="/register_creator">
                <button @click="register_as_creator()" type="submit" class="btn btn-success btn-lg btn-circle" data-bs-dismiss="modal" style="font-size: 20px;">+</button>
              </form>
            </div>
          </div>
        </div>
      </div>
  
      <div class="modal fade" id="rateModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h3 class="modal-title" id="RateTitle">Rate this song</h3>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="submitRating" method="post">
              <div class="modal-body">
                <div class="star-rating text-center">
                    <span v-for="rating in 5" :key="rating" class="star" :class="{ selected: rating <= selectedRating }" @click="selectRating(rating)">
                        &#9733;
                    </span>
                  <input type="hidden" name="rating" id="rating" v-model="selectedRating">
                  <input type="hidden" name="song_name" v-model="songNameModel">
                </div>
              </div>
  
              <div class="modal-footer">
                <button type="submit" class="btn btn-success btn-lg" data-bs-dismiss="modal" style="font-size: 20px;">Rate</button>
              </div>
            </form>
          </div>
        </div>
      </div>
  
      <div class="modal fade" id="commentModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h3 class="modal-title" id="commentTitle">Comment</h3>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="submitComment" method="post">
              <div class="modal-body">
                <textarea v-model="commentText" name="comment" id="comment" cols="60" rows="5" placeholder="What are Your Thoughts on this Song??"></textarea>
                <input type="hidden" name="song_name" v-model="songNameModel">
                <button type="submit" class="btn btn-success btn-lg" data-bs-dismiss="modal" style="font-size: 20px;">Post</button>
              </div>
  
              <div class="modal-footer" style="max-height: 300px; overflow-y: auto; display: block;">
                <div v-for="comment in comments" :key="comment.id">
                    <div class="card mb-3 w-100" style="width: 100%;">
                        <div class="card-body">
                            <h5 class="card-title">{{ comment[2] }}</h5>

                            <div class="text-end">
                                Ratings: {{ comment[3] }}/5
                            </div>
                        </div>

                        <div class="card-body">
                            {{ comment[4] }}
                        </div>
                    </div>
                </div>
              </div>
            </form>
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
        searchText: '',
        user_type: '',
        blacklisted: 0,
        song: null,
        selectedRating: 0,
        commentText: '',
        comments: []
      };
    },
    computed: {
        songNameModel() {
            return this.song ? this.song.name : '';
        }
    },
    methods: {
        async getData() {
            const username = localStorage.getItem('user'); // Fetch username from Local Storage
            const access_token = localStorage.getItem('access_token');
            if (!username) {
                console.error('Username not found in Local Storage');
                return;
            }

            const path = `http://127.0.0.1:5000/song/${this.$route.params.song_name}`;
            try {
                const res = await axios.get(path, {
                    headers: {
                        Authorization: `Bearer ${access_token}`
                    }
                });
                this.user_type = res.data.user_type;
                this.blacklisted = res.data.blacklisted;
                this.song = res.data.song;
                this.comments = res.data.comments;
            } catch (err) {
                console.error(err);
            }
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

            this.$router.push({ name: 'SongList', query: { searchResults: JSON.stringify(this.searchResults) } })
          })
          .catch(error => {
            console.error('Error searching:', error);
          });
        },
        selectRating(rating) {
            this.selectedRating = rating;
        },
        async submitRating() {
        // Implement this method to submit the rating
            const access_token = localStorage.getItem('access_token');
            if (!access_token) {
                console.error('Access token not found in Local Storage');
                return;
            }

            try {
                const res = await axios.post('http://127.0.0.1:5000/rate_song', {
                    song_name: this.song[1],
                    rating: this.selectedRating
                    }, {
                    headers: {
                        Authorization: `Bearer ${access_token}`
                    }
                });
                console.log(res.data.message); // Log the success message
            } catch (err) {
                console.error('Failed to submit rating:', err);
            }
        },
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
        async submitComment() {
            // Implement this method to submit a comment
            const access_token = localStorage.getItem('access_token');
            if (!access_token) {
                console.error('Access token not found in Local Storage');
                return;
            }

            try {
                const response = await axios.post('http://127.0.0.1:5000/comment_song', {
                song_name: this.song[1],
                comment: this.commentText
                }, {
                    headers: {
                        Authorization: `Bearer ${access_token}`
                    }
                });

                console.log('Comment submitted successfully');
                // Update the comments list with the new comment
                this.comments = response.data.comments;
                // Clear the comment input
                this.commentText = '';
            } catch (error) {
                console.error('Failed to submit comment:', error);
            }
        },
        async logout() {
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
                localStorage.removeItem('user_type');
                localStorage.removeItem('searchFor');
                
                this.$router.push("/");
            })
            .catch(error => {
                console.error('Logout failed:', error);
            });
        }
    },
    mounted(){
        this.getData();

        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js';
        script.integrity = 'sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL';
        script.crossOrigin = 'anonymous';
        document.body.appendChild(script);

        document.addEventListener('DOMContentLoaded', function() {
            const stars = document.querySelectorAll('.star');
            const ratingInput = document.getElementById('rating');

            stars.forEach(star => {
                star.addEventListener('click', () => {
                    const selectedRating = star.getAttribute('data-rating');
                    ratingInput.value = selectedRating;

                    stars.forEach(s => {
                        const sRating = s.getAttribute('data-rating');
                        if (sRating <= selectedRating) {
                            s.classList.add('selected');
                        } else {
                            s.classList.remove('selected');
                        }
                    });
                });

                star.addEventListener('mouseover', () => {
                    const selectedRating = star.getAttribute('data-rating');
                    stars.forEach(s => {
                        const sRating = s.getAttribute('data-rating');
                        if (sRating <= selectedRating) {
                            s.classList.add('hovered');
                        } else {
                            s.classList.remove('hovered');
                        }
                    });
                });

                star.addEventListener('mouseout', () => {
                    stars.forEach(s => {
                        s.classList.remove('hovered');
                    });
                });
            });
        });
    }
  };
</script>
  
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

.star-rating {
    font-size: 0;
}

.star-rating .star {
    font-size: 40px;
    cursor: pointer;
}

.star-rating .star:hover {
    color: gold;
}

.star-rating .star.selected {
    color: gold;
}
</style>