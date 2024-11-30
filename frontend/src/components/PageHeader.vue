<template>
  <div class="header">
    <router-link to="/" class="h1">HarmonicAI</router-link>
    <div class="header-menu">
      <router-link to="/Generate" class="header-list">Generator</router-link>
      <router-link to="/Library" class="header-list" v-if="user_info != null">Library</router-link>
      <router-link to="/Discover" class="header-list">Discover</router-link>
      <router-link to="/Account" class="header-list" v-if="!user_info">
        <img 
          v-show="!isHovered" 
          @mouseover="toggleHover(true)" 
          @mouseleave="toggleHover(false)" 
          src="@/assets/images/icon/icon-profile-white.svg" 
          alt="Profile Icon White" />
        <img 
          v-show="isHovered" 
          @mouseover="toggleHover(true)" 
          @mouseleave="toggleHover(false)" 
          src="@/assets/images/icon/icon-profile-blue.svg" 
          alt="Profile Icon Blue" />
      </router-link>
      <router-link to="/Account" class="header-list" v-if="user_info">
        <img v-if="user_info.profile_img" :src="profile_img"/>
        <img v-else src="@/assets/images/profile.png" />
      </router-link>
    </div>
  </div>
</template>


<style lang="scss">
  @import "@/assets/sass/component.scss";
</style>

<script setup>
  import { onMounted, ref } from 'vue';

  const isHovered = ref(false);
  const user_info = ref();
  const profile_img = ref();
  

  const toggleHover = (bool) => {
    isHovered.value = bool;
  }

  onMounted(() => {
  
    // Retrieve user information JSON string from session storage
    const userDataJSON = sessionStorage.getItem('userInfo');

    if(userDataJSON != null){
      // Parse JSON string back into an object
      const userData = JSON.parse(userDataJSON);
      user_info.value = userData._rawValue;
      if (user_info.value != null) {
        if (user_info.value.profile_img) {
          profile_img.value  = require(`@/assets/images/${user_info.value.profile_img}`);
        }
      }
    }
    
  })
</script>