<template>
    <div class="genre-page">
        <div class="genre-list">
            <div v-for="genre in genre_list" :key="genre.id" class="genre-list-item" @click="changePlaylist(genre.id)">
                <div class="genre-list-item-container" :class="{ 'selected': selected_genre && selected_genre.id === genre.id }">{{ genre.name }}</div>
            </div>
        </div>
        <div class="songlist" :style="{ backgroundImage: 'url(' + selected_genre.img + ')', backgroundSize: 'cover'}">
            <div class="songlist-header">
                <img :src="selected_genre.img"/>
                <div class="songlist-header-text">
                    <h2>{{ selected_genre.name }}</h2>
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
                    <div v-for="item, index in genre_playlist" :key="item.id" 
                    class="song-details" 
                    :class="{ 'selected': selected_song && selected_song.audio_filenames === item.audio_filenames }"
                    @click="playSong(item, index)">
                        <span class="no">{{ index + 1 }}</span>
                        <span class="name">{{ item.song_name }}</span>
                        <span>{{ item.duration }}</span>
                        <span>{{ item.date_created }}</span>
                    </div>
                </tbody>
            </table>
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
        <h3>{{ selected_song.song_name }}</h3>
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
  @import "@/assets/sass/genrepage.scss";
</style>

<script setup>
    import { onMounted, ref, watch } from 'vue';
    import { useRouter } from 'vue-router';

    const audioPlayer = ref(null);
    const genre_playlist = ref([]);
    const selected_song = ref(null);
    const selected_genre = ref({});
    const router = useRouter();
    const genre = ref(null);
    const isHovered = ref(false);
    const shuffle_play = ref(false);
    const repeat = ref(true);
    const user_info = ref();
    const isPlaying = ref(false);
    const playbackTime = ref(0);
    const audioDuration = ref(0);
    const listenerActive = ref(false);
    const audioLoaded = ref(false);
    const volume = ref(80);
    const currentSongIndex = ref(0);
    const songList = ref([]);

    
    const genre_list = ref([
    {
        id: 'pop',
        name: 'Pop',
        img: require("@/assets/images/album/pop-genre-cover.png")
    },
    {
        id: 'hiphop',
        name: 'Hip Hop',
        img: require("@/assets/images/album/hip-hop-genre-cover.png")
    },
    {
        id: 'rnb',
        name: 'R&B',
        img: require("@/assets/images/album/rnb-genre-cover.png")
    },
    {
        id: 'cinematic',
        name: 'Cinematic',
        img: require("@/assets/images/album/cinematic-genre-cover.png")
    },
    {
        id: 'electronic',
        name: 'Electronic',
        img: require("@/assets/images/album/electronic-genre-cover.png")
    },
    {
        id: 'jazz',
        name: 'Jazz',
        img: require("@/assets/images/album/jazz-genre-cover.png")
    },
    {
        id: 'indie',
        name: 'Indie',
        img: require("@/assets/images/album/indie-genre-cover.png")
    },
    {
        id: 'lofi',
        name: 'Lofi',
        img: require("@/assets/images/album/lofi-genre-cover.jpg")
    },
    {
        id: 'latin',
        name: 'Latin',
        img: require("@/assets/images/album/latin-genre-cover.png")
    },
    {
        id: 'rock',
        name: 'Rock',
        img: require("@/assets/images/album/rock-genre-cover.png")
    }]);

    const changePlaylist = (genre) => {
      // Find the genre details from genre_list
      const genreDetails = genre_list.value.find(g => g.id === genre);
      
      // Check if the genre details were found
      if (genreDetails) {
          // Assign the genre details to selected_genre
          selected_genre.value = genreDetails;
          router.push({ name: 'Genre', params: { genre: selected_genre.value.id } });
          // Fetch the playlist with the genre id
          fetchPlaylist(genreDetails.id);
      } else {
          console.error('Genre not found:', genre);
      }
    };

    const fetchPlaylist = async (genre) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/genre_playlist?genre=${genre}`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const months = [
                "January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"
            ];

            data.forEach(playlist => {
                const formatted = new Date(playlist.date_created);

                const day = formatted.getDate();
                const month = months[formatted.getMonth()];
                const year = formatted.getFullYear();

                playlist.date_created = `${day} ${month}, ${year}`;
            });

            genre_playlist.value = data;
            songList.value = [...genre_playlist.value];

        } catch (error) {
            console.error('Error fetching playlist:', error);
        }
    };

    const playSong = (song, index) => {
        if(song == null){
            song = songList.value[0];
        }
        // Construct the path to the audio file
        const filePath = require(`@/assets/audio/${song.audio_filenames}`);

        // Create an Audio object with the file path
        audioPlayer.value = new Audio(filePath);
        selected_song.value = song;
        isPlaying.value = true;
        audioLoaded.value = true;
        currentSongIndex.value = index;
    };

    // Get the genre from the route parameters
    const getGenreFromRoute = () => {
        return router.currentRoute.value.params.genre; // Return the genre value
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

    onMounted(() => {
        genre.value = getGenreFromRoute();
        changePlaylist(genre.value);
        
        // Retrieve user information JSON string from session storage
        const userDataJSON = sessionStorage.getItem('userInfo');

        // Parse JSON string back into an object
        user_info.value = JSON.parse(userDataJSON);

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