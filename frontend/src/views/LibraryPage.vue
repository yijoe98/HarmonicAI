<template>
    <div class="library-page">
      <div class="user-recommendation" v-if="recommend_song.length > 0">
        <h3>Recommended Songs</h3>
        <div class="recommend-container">
          <button 
            class="list"
            v-for="song, index in recommend_song" :key="index">
            <span class="no">{{ index + 1 }}</span>
            <span>{{ song.song_names }}</span>
            <span class="artist">{{ song.artist }}</span>
          </button>
        </div>
      </div>
      <div class="library">
        <div class="playlist">
          <div class="playlist-header">
            <img src="@/assets/images/icon/icon-library.svg" class="icon-library"/>
            <h2>Your Library</h2>
          </div>
          <div class="playlist-body">
            <button v-for="item, index in user_info.playlist" :key="index" class="playlist-body-item" @click="changePlaylist(item)">
              <div class="playlist-body-item-container" :class="{ 'selected': selectedPlaylist && selectedPlaylist.id === item.id }">
                <img :src="require(`@/assets/images/${item.playlist_cover}`)" />
                <div class="playlist-body-item-container-text">
                  <h3>{{ item.playlist_name }}</h3>
                  <span>{{ item.song_list.length + " songs" }}</span>
                  <span>{{ moment(item.date_created).format('MMMM DD, YYYY') }}</span>
                </div>
              </div>
            </button>
          </div>
        </div>
        <div class="songlist">
          <img :src="playlist_cover"/>
          <div class="songlist-header">
            <img :src="playlist_cover"/>
            <div class="songlist-header-text">
              <h2>{{ selectedPlaylist.playlist_name }}</h2>
              <h3 v-if="selectedPlaylist.song_list">{{ selectedPlaylist.song_list.length + ' songs' }}</h3>
              <h3>{{ moment(selectedPlaylist.date_created).format('MMMM DD, YYYY') }}</h3>
              <div class="action-icon">
                <div
                  @mouseover="isHovered = true"
                  @mouseleave="isHovered = false"
                >
                  <img 
                  class="play-btn" 
                  src="@/assets/images/icon/icon-play-white.png" 
                  v-if="!isHovered && !audioPlayer"
                  />
                  <img 
                  class="play-btn" 
                  src="@/assets/images/icon/icon-play-blue.png" 
                  v-if="isHovered || audioPlayer"
                  @click="playSong(null)"
                  />
                </div>
                <img v-if="!shuffle_play" @click="shufflePlay(true)" src="@/assets/images/icon/icon-shuffle-play-white.svg"/>
                <img v-else @click="shufflePlay(false)" src="@/assets/images/icon/icon-shuffle-play-blue.svg"/>
                <img v-if="!repeat" @click="repeatPlay(true)" src="@/assets/images/icon/icon-repeat-white.png"/>
                <img v-else @click="repeatPlay(false)" src="@/assets/images/icon/icon-repeat-blue.png"/>
              </div>
            </div>
          </div>

          <div class="songlist-body">
            <table>
              <thead>
                <h5 class="no">No</h5>
                <h5 class="name">Name</h5>
                <h5>Duration</h5>
                <h5>Date Added</h5>
              </thead>
              <tbody>
                <div v-for="item,index in selectedPlaylist.song_list" 
                :key="item.id" 
                class="song-details"
                :class="{ 'selected': selected_song && selected_song.song === item.song }"
                @click="playSong(item, index)">
                  <span class="no">{{ index+1 }}</span>
                  <span class="name">{{ item.song }}</span>
                  <span>{{ item.duration }}</span>
                  <span>{{ moment(item.date_created).format('MMMM DD, YYYY') }}</span>
                </div>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div class="audio-player-container" 
      v-if="audioPlayer"
      id="audio-player" >
      <audio 
        ref="audioPlayer" 
        :src="audioPlayer.src" 
        controls autoplay
        >
      </audio>

      <div class="details-container">
        <h3>{{ selected_song.song }}</h3>
        <div class="control-btn">
          <button @click="playPreviousSong">
            <img src="@/assets/images/icon/icon-previous-song.png"/>
          </button>
          <button @click="toggleAudio()">
            <img v-if="!isPlaying" src="@/assets/images/icon/icon-play-blue-no-border.png"/>
            <img v-else src="@/assets/images/icon/icon-pause-blue-no-border.png"/>
          </button>
          <button @click="playNextSong">
            <img src="@/assets/images/icon/icon-next-song.png"/>
          </button>
        </div>
        <div class="volume-slider-container">
          <img src="@/assets/images/icon/icon-volume-blue.png"/>
          <div class="volume-slider">
            <input type="range" v-model="volume" min="0" max="100" @input="adjustVolume">
          </div>
        </div>
      </div>

      <div
          id="progress-bar"
          class="progress-bar"
      >
          <input
              v-model="playbackTime"
              type="range"
              min="0"
              :max="audioDuration"
              class="slider"
              id="position"
              name="position"
              @input="adjustTimeline"
          />
          
          <div
              v-show="audioLoaded"
              class="time"
          >
              <span class="current">{{ elapsedTime() }}</span>

              <span class="total">{{ totalTime() }}</span>
              
          </div>
      </div>
    </div>
</template>

<style lang="scss">
  @import "@/assets/sass/librarypage.scss";
  
</style>

<script setup>
  import { onMounted, ref, watch } from 'vue';
  import moment from 'moment';


  const user_info = ref({});

  const selectedPlaylist = ref({});
  const playlist_cover = ref();
  const isHovered = ref(false);
  const shuffle_play = ref(false);
  const repeat = ref(true);
  const selected_song = ref({});
  const audioPlayer = ref(null);
  const isPlaying = ref(false);
  const playbackTime = ref(0);
  const audioDuration = ref(0);
  const listenerActive = ref(false);
  const audioLoaded = ref(false);
  const volume = ref(80);
  const currentSongIndex = ref(0);
  const songList = ref([]);
  const recommend_song = ref([]);

  // Function to change the playlist
  const changePlaylist = (playlist) => {
    selectedPlaylist.value = playlist;
    songList.value = [...selectedPlaylist.value.song_list]
    playlist_cover.value = require(`@/assets/images/${selectedPlaylist.value.playlist_cover}`);
  };

  // Function to shuffle play
  const shufflePlay = (bool) => {
    shuffle_play.value = bool;
    
    if(shuffle_play.value){
      for (let i = songList.value.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i+1));
          [songList.value[i], songList.value[j]] = [songList.value[j], songList.value[i]];
      }
    }
  };

  // Function to repeat play
  const repeatPlay = (bool) => {
    repeat.value = bool;
  };

  // Function to play a song
  const playSong = (song, index) => {
    if(song == null){
      song = songList.value[0];
    }
    const filePath = require(`@/assets/audio/${song.audio_filenames}`);

    // Create an Audio object with the file path
    audioPlayer.value = new Audio(filePath);
    selected_song.value = song;
    isPlaying.value = true;
    audioLoaded.value = true;
    currentSongIndex.value = index;
    updateListeningHistory(song.song);
  };
  
  const toggleAudio = () => {
      const audio = audioPlayer.value;
      if (audio.paused) {
          audio.play();
          isPlaying.value = true;
      } else {
          audio.pause();
          isPlaying.value = false;
      }
  };

  const initSlider = () => {
    const audio = audioPlayer.value;
    if (audio) {
        audioDuration.value = Math.round(audio.duration);
    }
  };

  const convertTime = (seconds) => {
      const format = val => `0${Math.floor(val)}`.slice(-2);
      const minutes = (seconds % 3600) / 60;
      return [minutes, seconds % 60].map(format).join(":");
  };

  const totalTime = () => {
      const audio = audioPlayer.value;
      if (audio) {
          const seconds = audio.duration;
          return convertTime(seconds);
      } else {
          return '00:00';
      }
  };

  const elapsedTime = () => {
      const audio = audioPlayer.value;
      if (audio) {
          const seconds = audio.currentTime;
          return convertTime(seconds);
      } else {
          return '00:00';
      }
  };

  const updateCurrentTime = () => {
      const audio = audioPlayer.value;
      if (audio) {
          playbackTime.value = audio.currentTime;
      }
  };

  const adjustVolume = () => {
    audioPlayer.value.volume = volume.value / 100;
  };

  const playPreviousSong = () => {
    if(currentSongIndex.value == 0){
      currentSongIndex.value = songList.value.length - 1;
    }
    else{
      currentSongIndex.value--;
    }
    playSong(songList.value[currentSongIndex.value], currentSongIndex.value);
  };

  const playNextSong = () => {
    if(repeat.value){
      if(currentSongIndex.value == songList.value.length - 1){
        currentSongIndex.value = 0;
        if(shuffle_play.value){
          shufflePlay(true);
        }
      }
      else{
        currentSongIndex.value++;
      }
      playSong(songList.value[currentSongIndex.value], currentSongIndex.value);
    }
    else{
      if(currentSongIndex.value == songList.value.length - 1){
        isPlaying.value = false;
        audioPlayer.value.pause();
      }
      else{
        currentSongIndex.value++;
        playSong(songList.value[currentSongIndex.value], currentSongIndex.value);
      }
    }
    
  };

  const adjustTimeline = () => {
    const newTime = audioPlayer.value.duration * (playbackTime.value / audioDuration.value);
    audioPlayer.value.currentTime = newTime;
  };

  const updateListeningHistory = async (songName) => {
      if (user_info.value) {
          try {

            if (!user_info.value.history) {
                user_info.value.history = [];
            }
            user_info.value.history = user_info.value.history.filter(song => song !== songName);
            user_info.value.history.unshift(songName);

            if (user_info.value.history.length > 10) {
                user_info.value.history = user_info.value.history.slice(0, 10);
            }
            const response = await fetch('http://127.0.0.1:8000/update_listening_history', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: user_info.value.username,
                    history: user_info.value.history
                })
            });

            if (!response.ok) {
                throw new Error('Failed to update listening history');
            }

            if(response.ok){
              sessionStorage.setItem('userInfo', JSON.stringify(user_info));
              retrieveUserInfo();
            }
          } catch (error) {
              console.error('Error updating listening history:', error);
          }
      }
  };

  const user_recommendation = async() => {
    if(user_info.value.history.length > 0){
      const combined_history = user_info.value.history.join(' ').trim()
      try {
          const response = await fetch(`http://127.0.0.1:8000/recommendation`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: combined_history })
          });

          if (!response.ok) {
          throw new Error('Network response was not ok');
          }

          const data = await response.json();
          recommend_song.value = data;

      } catch (error) {
          console.error('Error:', error);
          return [];
      }
    } else{
      recommend_song.value = [];
    }
  }

  const retrieveUserInfo = () => {
    const userDataJSON = sessionStorage.getItem('userInfo');

      // Parse JSON string back into an object
      const userData = JSON.parse(userDataJSON);
      user_info.value = userData._rawValue;

      selectedPlaylist.value = user_info.value.playlist[0];
      songList.value = [...selectedPlaylist.value.song_list];
      playlist_cover.value = require(`@/assets/images/${selectedPlaylist.value.playlist_cover}`);

  }

  onMounted(async() => {

    // Retrieve user information JSON string from session storage
    retrieveUserInfo();
    await user_recommendation();

    watch(audioPlayer, (newValue) => {
        if (newValue) {
            const audio = newValue;
            audio.addEventListener("loadedmetadata", () => {
                initSlider();
            });
            audio.addEventListener("canplay", () => {
                audioLoaded.value = true;
            });
            watch(playbackTime, (newVal) => {
                const diff = Math.abs(playbackTime.value - audio.currentTime);
                if (diff > 0.01) {
                    newVal = playbackTime.value;
                }

                if (newVal) {
                    initSlider();
                    if (!listenerActive.value) {
                        listenerActive.value = true;
                    }
                }
            });
            audio.addEventListener("timeupdate", () => {
              if (audio.currentTime >= audio.duration) {
                  // Call playNextSong() when the song has ended
                  playNextSong();
              }
            });
            setInterval(updateCurrentTime, 500);
        }
    });
  });

  

</script>

