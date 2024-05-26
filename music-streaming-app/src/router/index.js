import { createRouter, createWebHistory } from "vue-router";
import WelcomePage from "../components/WelcomePage.vue";
import HomePage from "../components/HomePage.vue";
import LoginPage from "../components/LoginPage.vue";
import RegisterPage from "../components/RegisterPage.vue";
import AdminLoginPage from "../components/AdminLoginPage.vue";
import CreatorPage from "../components/CreatorPage.vue";
import UploadSong from "../components/UploadSong.vue";
import EditSong from "../components/EditSong.vue";
import SongDetails from "../components/SongDetails.vue";
import AdminPage from "../components/AdminPage.vue";
import CreatorList from "../components/CreatorList.vue";
import TracksRecord from "../components/TracksRecord.vue";
import SongList from "../components/SongList.vue";
import PlaylistDetails from "../components/PlaylistDetails.vue";
import AlbumDetails from "../components/AlbumDetails.vue";

const routes = [
  {
    path: "/",
    name: "WelcomePage",
    component: WelcomePage,
  },
  {
    path: "/register",
    name: "RegisterPage",
    component: RegisterPage,
  },
  {
    path: "/login",
    name: "LoginPage",
    component: LoginPage,
  },
  {
    path: "/adminlogin",
    name: "AdminLoginPage",
    component: AdminLoginPage,
  },
  {
    path: "/home",
    name: "HomePage",
    component: HomePage,
  },
  {
    path: "/creator",
    name: "CreatorPage",
    component: CreatorPage,
    meta: { requiresCreator: true },
  },
  {
    path: "/upload",
    name: "UploadSong",
    component: UploadSong,
    meta: { requiresCreator: true },
  },
  {
    path: "/edit_song/:song_id",
    name: "EditSong",
    component: EditSong,
    meta: { requiresCreator: true },
  },
  {
    path: "/song/:song_name",
    name: "SongDetails",
    component: SongDetails,
  },
  {
    path: "/admin",
    name: "AdminPage",
    component: AdminPage,
    meta: { requiresAdmin: true },
  },
  {
    path: "/usermanagement",
    name: "CreatorList",
    component: CreatorList,
    meta: { requiresAdmin: true },
  },
  {
    path: "/tracks",
    name: "TracksRecord",
    component: TracksRecord,
    meta: { requiresAdmin: true },
  },
  {
    path: "/search",
    name: "SongList",
    component: SongList,
  },
  {
    path: "/playlist/:playlist_id",
    name: "PlaylistDetails",
    component: PlaylistDetails,
  },
  {
    path: "/album/:album_id",
    name: "AlbumDetails",
    component: AlbumDetails,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to restrict access based on user type
router.beforeEach((to, from, next) => {
  const userType = localStorage.getItem("user_type"); // Assuming user_type is stored in localStorage

  // Check if the route requires admin access
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (userType === "admin") {
      next(); // User is admin, allow access
    } else {
      next({ name: "HomePage" }); // Redirect to login page if not admin
    }
  } else if (to.matched.some(record => record.meta.requiresCreator)) {
    if (userType !== "user") {
      next(); // User is a regular user, allow access
    } else {
      next({ name: "HomePage" }); // Redirect to login page if not a regular user
    }
  } else {
    next(); // No restriction, allow access
  }
});

export default router; // Make sure to export the router instance
