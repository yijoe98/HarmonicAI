// import Vue from 'vue'
// import VueRouter from 'vue-router'
import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/HomePage.vue';
import Generate from '@/views/GeneratePage.vue';
import Library from '@/views/LibraryPage.vue';
import Account from '@/views/ProfilePage.vue';
import Genre from '@/views/GenrePage.vue';
import Discover from '@/views/DiscoverPage.vue';



const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/Generate',
    name: 'Generate',
    component: Generate,
    meta: { hideFooter: true }
  },
  {
    path: '/Library',
    name: 'Library',
    component: Library,
    meta: { hideFooter: true }
  },
  {
    path: '/Account',
    name: 'Account',
    component: Account,
    meta: { hideFooter: true }
  },
  {
    path: '/Discover/Genre/:genre',
    name: 'Genre',
    component: Genre,
    meta: { hideFooter: true }
  },
  {
    path:'/Discover',
    name:'Discover',
    component: Discover
  }
]


const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      };
    }
    return { top: 0 };
  },
});

export default router