<template>
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    </head>
    <body>
      <div class="container-fluid">
        <nav class="navbar navbar-expand-lg justify-content-between border-bottom border-dark">
          <div class="navbar-brand">
            <h3>Music Streaming Application</h3>
          </div>
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/adminlogin">App Admin</router-link>
            </li>
          </ul>
        </nav>

        <br /><br /><br /><br />

        <div class="row">
          <h1 align="center">
            <font size="+5">Welcome to Music Streaming Application</font>
          </h1>
          <br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
          <div class="row p-5">
            <div class="d-grid gap-2 col-5 justify-content-md-end">
              <button type="button" class="btn btn-primary btn-lg">
                <router-link to="/login" class="text-light text-decoration-none"
                  >Login</router-link
                >
              </button>
            </div>

            <div class="d-grid gap-2 col-3 justify-content-md-end">
              <button type="button" class="btn btn-secondary btn-lg">
                <router-link to="/register" class="text-light text-decoration-none"
                  >Register</router-link
                >
              </button>
            </div>
          </div>
        </div>
      </div>
    </body>
  </html>
</template>

<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
</style>
