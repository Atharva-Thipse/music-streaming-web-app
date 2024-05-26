<template>
    <div class="container-fluid">
      <nav class="navbar navbar-expand-lg border-bottom border-dark">
        <div class="navbar-brand">
          <h3>Music Streaming Application</h3>
        </div>
      </nav>
  
      <br><br><br><br>
  
      <div class="row">
        <h1 align="center"><font size="+5">Admin Login</font></h1>
        <br><br><br>
      </div>
  
      <div class="row">
        <form class="form" @submit.prevent="login" method="post" action="/admin_login_validation">
          <div class="d-grid col-7 justify-content-md-end">
            <h3>Username</h3>
            <input v-model="username" type="text" class="form-control" size="30" name="admin_login_username">
          </div>
  
          <div class="d-grid col-7 justify-content-md-end">
            <br>
            <h3>Password</h3>
            <input v-model="password" type="password" class="form-control" size="30" name="admin_login_password">
          </div>
  
          <div class="row p-5">
            <div class="text-center">
              <button type="submit" class="btn btn-success btn-lg" value="AdminLogin">Login</button>
            </div>
          </div>
        </form>
      </div>
  
      <br>
      
      <p align="center">Don't have admin access? Go to <router-link to="/login">User Login</router-link></p>     
    </div>
  </template>
  
<script>
import axios from 'axios';

export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },

    methods: {
      async login() {
        try {
          // Send a POST request to the server with the username and password
          const response = await axios.post('http://127.0.0.1:5000/admin_login_validation', {
            admin_login_username: this.username,
            admin_login_password: this.password
          });
          
          // If the request is successful, store the access token, user, and user type in localStorage
          localStorage.setItem('access_token', response.data.access_token);
          localStorage.setItem('user', response.data.user);
          localStorage.setItem('user_type', response.data.user_type);

          this.$router.push("/admin");
        
        } catch (error) {
          console.error(error.message);
        }
      }
    }
};
</script>

<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
</style>
