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
            <form @submit.prevent="register_user" class="form">
                <div class="d-grid col-7 justify-content-md-end">
                    <label for="username"></label>
                    <h3>Enter Username</h3>
                    <input v-model="username" type="text" class="form-control" size="30" name="register_username" required />
                </div>

                <div class="d-grid col-7 justify-content-md-end">
                    <label for="email"></label>
                    <br>
                    <h3>Enter Email</h3>
                    <input v-model="email" type="email" class="form-control" size="30" name="register_email" required />
                </div>

                <div class="d-grid col-7 justify-content-md-end">
                    <br>
                    <h3>Enter Password</h3>
                    <input v-model="password" type="password" class="form-control" size="30" name="register_password" required />
                </div>

                <div class="d-grid col-7 justify-content-md-end">
                    <br>
                    <h3>Confirm Password</h3>
                    <input v-model="confirmPassword" type="password" class="form-control" size="30" name="confirm_password" required />
                    <span v-if="!passwordsMatch && isConfirmPasswordNotEmpty" class="text-danger">Password Doesn't Match</span>
                </div>

                <div class="row p-5">
                    <div class="text-center">
                        <button type="submit" class="btn btn-secondary btn-lg" value="Register" :disabled="!passwordsMatch || !isPasswordNotEmpty">Register</button>
                    </div>
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

export default{
    data(){
        return{
            username: '',
            password: '',
            confirmPassword: '',
            email: '',
            errorMessage: '',
        };
    },

    computed: {
        passwordsMatch() {
            return this.confirmPassword === this.password;
        },
        isPasswordNotEmpty() {
            return this.password.trim() !== '';
        },
        isConfirmPasswordNotEmpty() {
            return this.confirmPassword.trim() !== '';
        },
    },

    methods: {
        async register_user(){
            try{
                const response = await axios.post('http://127.0.0.1:5000/register_user', {
                    username: this.username,
                    password: this.password,
                    email: this.email,
                });
                console.log("Signup Successful",response.data);
                this.$router.push("/login");
            }catch(error){
                this.errorMessage = error.response.data.error;
                console.error(this.errorMessage);
            }
        }
    }
}
</script>