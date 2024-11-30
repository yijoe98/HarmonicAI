<template>
    <div class="discover-page">
        <div class="carousel">
            <el-carousel :interval="4000" arrow="never" motion-blur="true" indicator-position="outside" autoplay="true">
                <el-carousel-item 
                v-for="item in carousel_list" :key="item"
                :style="{ backgroundImage: 'url(' + item.image + ')', backgroundSize: 'cover'}">
                    <div class="carousel-content">
                        <div class="carousel-content-container">
                            <h3>{{ item.header }}</h3>
                            <span>{{ item.description }}</span>
                            <button @click="scrollToSection(item.id)">Explore</button>
                        </div>
                    </div>
                </el-carousel-item>
            </el-carousel>
        </div>

        <section class="genre" :id="4">
            <h3>Genres</h3>
            <div class="genre-list">
                <router-link :to="'/Discover/Genre/' + genre.id"  v-for="genre in genre_list" :key="genre.id" 
                    class="genre-list-item">
                    <img :src="genre.img" />
                    <span>{{ genre.name }}</span>
                </router-link>
            </div>
        </section>

        <section class="song-recommender" :id="1">
            <h3>Song Recommendations</h3>
            <div class="input">
                <div class="input-wrapper">
                    <input
                        v-model="search"
                        placeholder="Search some song..."
                        class="search-input"
                    />
                    <img @click="submitSearch" src="@/assets/images/icon/icon-search.png" class="search-icon" />
                </div>
            </div>
            <div class="result" v-if="recommend_song.length > 0">
                <h4>Results</h4>
                <div class="result-container">
                    <button 
                        class="list"
                        v-for="song, index in recommend_song" :key="index">
                        <span class="no">{{ index + 1 }}</span>
                        <div class="song-details" @click="listenSong(song.track_id, song.song_names)">
                            <span>{{ song.song_names }}</span>
                            <span class="artist">{{ song.artist }}</span>
                        </div>
                    </button>
                </div>
                
            </div>
            <div v-else class="result-empty">
                <img src="@/assets/images/icon/icon-empty.png"/>
                <span>No results found.</span>
            </div>
        </section>

        <section class="popular-artist" :id="2">
            <h3>Popular Artists</h3>
            <div class="popular-artist-container">
                <div class="popular-artist-container-item" v-for="item, index in popular_artist" :key="index"
                :class="{ 'index-1': index === 0, 'index-2': index === 1 , 'index-3': index === 2  }">
                    <div class="text-effect-wrapper">
                        <h1 class="text" contenteditable>{{ index+1 }}</h1>
                    </div>
                    <div class="title">
                        <h2>{{ item.track_artist }}</h2>
                    </div>
                    <div class="artist-playlist">
                        <div class="artist-playlist-container">
                            <div class="item" 
                                v-for="song, num in artist_playlist[index+1]"
                                :key="num"
                                @click="listenSong(song.track_id, song.track_name)">
                                <p class="num">{{ num+1 }}</p>
                                <p>{{ song.track_name }}</p>
                                <p class="listen-count">{{ formatNumber(song.listen_count, song.track_name) }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="popular-song" :id="3">
            <h3>Popular Songs</h3>
            <div class="popular-song-body">
                <div class="popular-song-body-container">
                    <div
                        v-for="item, index in popular_song" :key="item.id"
                        class="song-item">
                        <p class="num">{{ index+1 }}</p>
                        <div class="content" @click="listenSong(item.track_id, item.track_name)">
                            <p v-if="item && item.track_name">{{ capitalizeFirstLetter(item.track_name) }}</p>
                            <p class="name">{{ item.track_artist }}</p>
                            <p class="name">{{ item.listen_count ? formatNumber(item.listen_count) : '0'  }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <div class="iframe">
            <iframe id="spotifyPlayer" width="1490" height="175" frameborder="0" allowtransparency="false" allow="encrypted-media"></iframe>
        </div>
    </div>
</template>

<style lang="scss">
  @import "@/assets/sass/discoverpage.scss";
</style>

<script setup>
    import { RouterLink } from 'vue-router';
    import { ref, onMounted } from 'vue';

    const popular_song = ref([{}]);
    const popular_artist = ref([{}]);
    const artist_playlist = ref([{}]);
    const search = ref('');
    const recommend_song = ref([]);
    const spotifyEmbedUrl = ref();
    const user_info = ref({});
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

    const carousel_list = ref([
        {
            id: 1,
            image: require("@/assets/images/carousel-recommender.jpg"),
            header: "Curated for You",
            description: "Enjoy a personalized music experience! Our Discover page uses your listening habits to recommend songs, artists, and genres tailored to your taste."
        },
        {
            id: 2,
            image: require("@/assets/images/carousel-artist.jpg"),
            header: "Top Artists Spotlight",
            description: "Discover the artists making waves in the music world. From chart-topping legends to rising stars, find your new favorite musicians right here."
        },
        {
            id: 3,
            image: require("@/assets/images/carousel-song.jpg"),
            header: "Explore Popular Songs",
            description: "Stay updated with the latest hits! Our Discover page brings you the most popular songs, ensuring you never miss out on the tracks everyone is talking about."
        },
        {
            id: 4,
            image: require("@/assets/images/carousel-genre.jpg"),
            header: "Dive into Genres",
            description: "Whether you're a fan of pop, rock, hip-hop, or jazz, our Discover page has a comprehensive genre list to help you explore and enjoy the diverse world of music."
        },
    ]);

    const formatNumber = (value) => {
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ", ");
    }

    const scrollToSection = (sectionId) => {
        // Get the selected section element using its ID
        const sectionElement = document.getElementById(sectionId.toString());
        if (sectionElement) {
            // Scroll to the selected section smoothly
            sectionElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    const updateListenCount = async(trackId) => {
        try {
            const response = await fetch('http://127.0.0.1:8000/update_listen_count', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    track_id: trackId
                })
            });

            if (!response.ok) {
                throw new Error('Failed to update listen count');
            }

            if(response.ok){
                await getPopularArtist();
                await getPopularSong();
            }

        } catch (error) {
            console.error('Error updating listen count:', error);
        }
    }

    const listenSong = async(track_id, song_name) => {
        spotifyEmbedUrl.value = "https://open.spotify.com/embed/track/" + track_id + "?autoplay=1";
        document.getElementById("spotifyPlayer").src = spotifyEmbedUrl.value;
        updateListenHistory(song_name);
        await updateListenCount(track_id);
    }

    const retrieveUserInfo = () => {
        const userDataJSON = sessionStorage.getItem('userInfo');

        // Parse JSON string back into an object
        const userData = JSON.parse(userDataJSON);
        user_info.value = userData._rawValue;

    }

    const updateListenHistory = async(songName) => {
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

          console.log(user_info.value.history);
              // Send POST request to update listening history
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
    }

    const getPopularSong = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/popular_song`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            popular_song.value = data;

        } catch (error) {
            console.error('Error fetching playlist:', error);
        }
    };

    const getPopularArtist = async() => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/popular_artist`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            popular_artist.value = data;

            popular_artist.value.forEach(async (song) => {
                const playlist = await getArtistPlaylist(song.track_artist);
                artist_playlist.value.push(playlist);
            });

        } catch (error) {
            console.error('Error fetching playlist:', error);
        }

    }

    const getArtistPlaylist = async(artist) => {
        try{
            const response = await fetch(`http://127.0.0.1:8000/artist_playlist/?artist=${artist}`, {
                method: 'GET',
                header:{
                    'Content-Type': 'application/json', 
                }
            }) 
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Error fetching playlist:', error);
        }
    }

    const submitSearch = async() => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/recommendation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: search.value })
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
    }

    const capitalizeFirstLetter = (string) => {
        let words = string.split(' ');

        for (let i = 0; i < words.length; i++) {
        words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1).toLowerCase();
        }

        return words.join(' ');
    }

    onMounted(async() => {
        await getPopularSong();
        await getPopularArtist();
        // Retrieve user information JSON string from session storage
        const userDataJSON = sessionStorage.getItem('userInfo');

        if(userDataJSON != null){
        // Parse JSON string back into an object
        const userData = JSON.parse(userDataJSON);
        user_info.value = userData._rawValue;
        }
    });
</script>