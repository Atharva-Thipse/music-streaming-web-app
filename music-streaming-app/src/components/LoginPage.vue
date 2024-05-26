<template>
    <div class="container-fluid">
      <nav class="navbar navbar-expand-lg border-bottom border-dark">
        <div class="navbar-brand">
          <h3>Music Streaming Application</h3>
        </div>
      </nav>
  
      <br><br>
        
        <div v-if="errorMessage" class="alert alert-danger d-flex align-items-center" role="alert">
            <div>
                {{ errorMessage }}
            </div>
        </div>
        
      <br><br>
  
      <div class="row">
        <h1 align="center"><font size="+5">User Login</font></h1>
        <br><br><br>
      </div>
  
      <div class="row">
        <form class="form" @submit.prevent="login" method="post" action="/login_validation">
          <div class="d-grid col-7 justify-content-md-end">
            <h3>Username</h3>
            <input v-model="username" type="text" class="form-control" size="28" name="login_username" required />
          </div>
  
          <div class="d-grid col-7 justify-content-md-end">
            <br>
            <h3>Password</h3>
            <input v-model="password" type="password" class="form-control" size="28" name="login_password" required />
          </div>
  
          <div class="row p-5">
            <div class="d-grid gap-2 col-5 justify-content-md-end">
              <button type="submit" class="btn btn-success btn-lg" style="width: 100px;">Login</button>
            </div>
  
            <div class="d-grid gap-2 col-3 justify-content-md-end">
              <button type="button" class="btn btn-secondary btn-lg" style="width: 100px;"><router-link to="/register" class="text-light text-decoration-none">Register</router-link></button>
            </div>
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
      username: '',
      password: '',
      errorMessage: ''
    };
  },

  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login_validation', {
          login_username: this.username,
          login_password: this.password
        });

        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('user', response.data.user);
        localStorage.setItem('user_type', response.data.user_type);

        this.$router.push("/home");
        
      }
      catch (error) {
        this.errorMessage = error.response.data.error;
        console.error(this.errorMessage);
      }
    }
  }
};
</script>
  
<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
</style>
  