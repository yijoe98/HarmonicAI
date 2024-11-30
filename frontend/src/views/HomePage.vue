<template>
  <div class="page">

    <div class="title">
      <video autoplay loop muted ref="videoPlayer">
        <source :src="videoPath" type="video/mp4">
      </video>

      <h1>HarmonicAI</h1>
    </div>

    <div class="website-description">
      <img src="@/assets/images/homepage1.jpg"/>
      <h1 ref="typingText">Where creativity meets technology, offering an AI music generator, an extensive library, trending discoveries, and personalized recommendations.</h1>
    </div>

    <div class="generate-section">
      <div class="section-left" data-aos="fade-right">
        <video autoplay loop muted ref="videoPlayer1">
          <source :src="videoPath1" type="video/mp4">
        </video>
      </div>
      <div class="description" data-aos="fade-left">
        <h1>Text-to-Music Generator</h1>
        <span>Transform your thoughts into melodies with our text-to-music feature. Simply input your words, and watch as they come to life in harmonious tunes, bridging the gap between language and melody seamlessly.</span>
        <router-link to="/Generate" class="generate-button">Try Now</router-link>
      </div>
    </div>

    <div class="library-section">
      <div class="container-left" data-aos="fade-right">
        <h1>Library and Personal Playlist</h1>
        <p>A personalized playlist just for you - enjoy your private collection.</p>
        <router-link to="/Library" class="library-button" v-if="user_info != null">View Library</router-link>
        <router-link to="/Account" class="library-button" v-else>Log In</router-link>
      </div>
      <div class="container-right" data-aos="fade-left">
        <img  src="@/assets/images/library-section.jpg"/>
      </div>
    </div>

    <div class="discover-section">

      <div class="container">
        <div class="card" data-aos="fade-up" data-aos-anchor-placement="center-bottom">
          <div class="face face1">
            <div class="content">   
              <img src="@/assets/images/homepage-genre.png"/>         
              <h3>Genre</h3>
            </div>
          </div>
          <div class="face face2">
            <div class="content">
              <p>Genre Playlists are collections of songs grouped based on their musical genre. These playlists cater to various musical tastes and preferences, providing users with a curated list of songs that share similar characteristics. </p>
              <router-link to="/Discover#4">Discover</router-link>
            </div>
          </div>
        </div>

        <div class="card" data-aos="fade-up" data-aos-anchor-placement="center-bottom">
          <div class="face face1">
            <div class="content">
              <img src="@/assets/images/homepage-artist.png"/>                
              <h3>Popular Artist</h3>
            </div>
          </div>
          <div class="face face2">
            <div class="content">
              <p>Popular Artists are musicians who have achieved significant fame and recognition in the music industry. These artists typically have a large following, produce high-selling records, and are influential in their genre.</p>
              <router-link to="/Discover#2">Discover</router-link>
            </div>
          </div>
        </div>

        <div class="card" data-aos="fade-up" data-aos-anchor-placement="center-bottom">
          <div class="face face1">
            <div class="content">    
              <img src="@/assets/images/homepage-song.jpg"/>            
              <h3>Popular Song</h3>
            </div>
          </div>
          <div class="face face2">
            <div class="content">
              <p>Popular Songs are tracks that are currently trending and widely listened to by a large audience. These songs often dominate charts and are frequently played on radio stations, music streaming platforms, and social media.</p>
              <router-link to="/Discover#3">Discover</router-link>
            </div>
          </div>
        </div>

        <div class="card" data-aos="fade-up" data-aos-anchor-placement="center-bottom">
          <div class="face face1">
            <div class="content">
              <img src="@/assets/images/homepage-recommendation.jpg"/>                
              <h3>Recommendations</h3>
            </div>
          </div>
          <div class="face face2">
            <div class="content">
              <p>The Search Function allows users to find specific songsvwithin a music platform. This feature is essential for navigating large music libraries and quickly accessing desired content.</p>
              <router-link to="/Discover#1">Discover</router-link>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style lang="scss">
  @import "@/assets/sass/homepage.scss";
  
</style>

<script setup>
  import { onMounted, ref } from 'vue';
  import { RouterLink } from 'vue-router';
  import AOS from 'aos';
  import 'aos/dist/aos.css';

  const videoPlayer = ref();
  const videoPath = require('@/assets/videos/homepage.mp4');
  const videoPlayer1 = ref();
  const videoPath1 = require('@/assets/videos/generator_section.mp4');
  const user_info = ref();
  const typingText = ref(null);

  const typeEffect = (element, speed, pause) => {
    const text = element.innerHTML;
    element.innerHTML = "";

    let i = 0;

    const type = () => {
      const timer = setInterval(async () => {
        if (i < text.length) {
          element.append(text.charAt(i));
          const lastChar = element.childNodes[element.childNodes.length - 1];
          const range = document.createRange();
          range.selectNodeContents(lastChar);
          i++;
        } else {
          clearInterval(timer);
          setTimeout(erase, pause);
        }
      }, speed);
    }

    const erase = () => {
      const timer = setInterval(async () => {
        if (i > 0) {
          element.innerHTML = element.innerHTML.substring(0, element.innerHTML.length - 1);
          if (element.childNodes.length > 0) {
            const lastChar = element.childNodes[element.childNodes.length - 1];
            const range = document.createRange();
            range.selectNodeContents(lastChar);
          }
          i--;
        } else {
          clearInterval(timer);
          setTimeout(type, pause);
        }
      }, speed);
    }

    type();
  } 

  onMounted(() => {
    const video = videoPlayer.value;
    video.muted = true;
    video.play();

    const video1 = videoPlayer1.value;
    video1.muted = true;
    video1.play();

    if (typingText.value) {
      typeEffect(typingText.value, 60, 500);
    }

    AOS.init({
      duration: 1800,
    });

    // Retrieve user information JSON string from session storage
    const userDataJSON = sessionStorage.getItem('userInfo');

    if(userDataJSON != null){
      // Parse JSON string back into an object
      const userData = JSON.parse(userDataJSON);
      user_info.value = userData._rawValue;
    }

  });
</script>