<template>
  <div class="generate-page">
    <div class="video">
      <video autoplay loop muted ref="videoPlayer2">
        <source :src="videoPath2" type="video/mp4">
      </video>
    </div>

    <h1>Generate your music through AI</h1>

    <div class="md-filter">
      <div class="md-filter-container">
        <div class="button">
          <button @click="showGenreList()">
            <span>{{ genre_input.name }}</span>
            <img :class="{ 'open': isShowGenreList }" src="@/assets/images/icon/icon-expand.png"/>
          </button>
          <div class="option-list" v-if="isShowGenreList" data-aos="fade-down"> 
            <div 
              v-for="genre, index in genre_list" :key="index"
              class="item"
              @click="selectGenre(genre)">
              <span v-if="genre.name !== 'Genre'">{{ genre.name }}</span>
              <span v-else>Clear All</span>
            </div>
          </div>
        </div>
        <div class="button">
          <button @click="showMoodList()">
            <span>{{ mood_input.name }}</span>
            <img :class="{ 'open': isShowMoodList }" src="@/assets/images/icon/icon-expand.png"/>
          </button>
          <div class="option-list" v-if="isShowMoodList" data-aos="fade-down">
            <div 
              v-for="mood, index in mood_list" :key="index"
              class="item"
              @click="selectMood(mood)">
              <span v-if="mood.name !== 'Mood'">{{ mood.name }}</span>
              <span v-else>Clear All</span>
            </div>
          </div>
        </div>
        <button @click="submitFilter"><span>Filter</span></button>
      </div>
      <div class="md-result-container">
        <div 
          class="result-item"
          v-for="result, index in mdResult.slice(0, 2)" :key="index"
          :class="{ 'selected': result.music_description === musicDescription}"
          @click="selectMusicDescription(result.music_description)">
          <span>{{ result.music_description }}</span>
        </div>
      </div>
    </div>
    
    <div class="input-box">
      <el-input
        v-model="musicDescription"
        :rows="3"
        type="textarea"
        placeholder="Please enter your prompt..."
      />
    </div>
    
    <button @click="generateMusic" v-if="current_status === 1">Generate</button>
    <button @click="generateMusic" v-if="current_status === 2">Regenerate</button>
  </div>
  <div class="audio-player-container" 
    v-if="audioPlayer && current_status === 2"
    id="audio-player" >
    <audio 
      ref="audioPlayer" 
      :src="audioPlayer.src" 
      controls autoplay
      >
    </audio>

    <div class="details-container">
      <h3>
        {{ song_name }}
        <button @click="downloadMusic()">
          <img src="@/assets/images/icon/icon-download.png"/>
        </button>
      </h3>
      
      <div class="control-btn">
        <button @click="toggleAudio()">
          <img v-if="!isPlaying" src="@/assets/images/icon/icon-play-blue-no-border.png"/>
          <img v-else src="@/assets/images/icon/icon-pause-blue-no-border.png"/>
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
    @import "@/assets/sass/generatepage.scss";
  </style>
  
  <script setup>
  import { onMounted, ref, watch } from 'vue';
  import AOS from 'aos';
  import 'aos/dist/aos.css';
  
  //data
  const current_status = ref();
  const musicDescription = ref();
  const audioPlayer = ref(null);
  const videoPlayer2 = ref(null);
  const videoPath2 = require('@/assets/videos/generate-page.mp4');
  const isPlaying = ref(false);
  const playbackTime = ref(0);
  const audioDuration = ref(0);
  const listenerActive = ref(false);
  const audioLoaded = ref(false);
  const volume = ref(80);
  const song_name = ref();
  const genre_input = ref({name: 'Genre', value:''});
  const mood_input = ref({name: 'Mood', value:''});
  const isShowGenreList = ref(false);
  const isShowMoodList = ref(false);
  const mdResult = ref([]);

  const genre_list = ref([
    {
      name: 'Cinematic',
      value: 'cinematic'
    },
    {
      name: 'Hip Hop',
      value: 'hiphop'
    },
    {
      name: 'Jazz',
      value: 'jazz'
    },
    {
      name: 'Lofi',
      value: 'lofi'
    },
    {
      name: 'Rock',
      value: 'rock'
    },
    {
      name: 'Genre',
      value: ''
    }
    
  ])

  const mood_list = ref([
    {
      name: 'Action',
      value: 'action'
    },
    {
      name: 'Ambient',
      value: 'ambient'
    },
    {
      name: 'Depression',
      value: 'depression'
    },
    {
      name: 'Energetic',
      value: 'energetic'
    },
    {
      name: 'Happy',
      value: 'happy'
    },
    {
      name: 'Mood',
      value: ''
    }
  ])

  const selectMusicDescription = (music_description) => {
    musicDescription.value = music_description;
  }

  const showGenreList = () => {
    isShowGenreList.value = !isShowGenreList.value;
  }

  const showMoodList = () => {
    isShowMoodList.value = !isShowMoodList.value;
  }

  const selectGenre = (genre) => {
    genre_input.value = genre;
    isShowGenreList.value = !isShowGenreList.value;
  }

  const selectMood = (mood) => {
    mood_input.value = mood;
    isShowMoodList.value = !isShowMoodList.value;
  }

  const submitFilter = async() => {
    try{
      const response = await fetch('http://127.0.0.1:8000/music_description', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          genre: genre_input.value.value,
          mood: mood_input.value.value
        })
      });

      const data = await response.json();
      mdResult.value = data;

      for(let i = mdResult.value.length -1; i>0; i-- ){
        const j = Math.floor(Math.random() * (i+1));
        [mdResult.value[i], mdResult.value[j]] = [mdResult.value[j], mdResult.value[i]];
      }

    }

    catch(error){
      console.error('There was an error!', error);
    }
  }
  
  const generateMusic = async() => {
    current_status.value = 2; 
    const response = await fetch('http://127.0.0.1:8000/generate_audio', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        
      },
      body: JSON.stringify({
        "music_desc": musicDescription.value,
      })
    });

    const arrayBuffer = await response.arrayBuffer();
    const blob = new Blob([arrayBuffer], { type: 'audio/wav' });
    const audioUrl = URL.createObjectURL(blob);

    if (!audioUrl.value) {
      song_name.value = musicDescription.value;
      audioPlayer.value = new Audio(audioUrl);
      playSong();
    }
  }

  const downloadMusic = () => {
    const link = document.createElement('a');

    link.href = audioPlayer.value.src;
    link.download = `${musicDescription.value}.wav`; 

    link.click();
  };

  const playSong = () => {
      isPlaying.value = true;
      audioLoaded.value = true;
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

    const adjustTimeline = () => {
        const newTime = audioPlayer.value.duration * (playbackTime.value / audioDuration.value);
        audioPlayer.value.currentTime = newTime;
    };

  onMounted(() => {
    current_status.value = 1;
    playSong();
    const video2 = videoPlayer2.value;
    if (video2) {
      video2.muted = true;
      video2.play();
    } else {
      console.error('Video element not found');
    }

    AOS.init({
      duration: 400,
    });

    submitFilter();
  });

 

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
            setInterval(updateCurrentTime, 500);
        }
    });
  </script>
    
      