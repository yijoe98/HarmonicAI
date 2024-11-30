<template>
    <div class="profile-page">
        <div class="error-message" v-if="error_msg" data-aos="fade-down" data-aos-duration="600">
            <p>{{ error_msg }}</p>
        </div>
        <div class="success-message" v-if="success_msg" data-aos="fade-down" data-aos-duration="600">
            <p>{{ success_msg }}</p>
        </div>

        <div class="login-modal" v-if="!isLogin">
            <div class="login-modal-container" data-aos="fade-up">
                <router-link to="/" class="close-btn">
                    <img src="@/assets/images/icon/icon-close.png"/>
                </router-link>
                <img class="bg" src="@/assets/images/login.jpg"/>
                <div class="content">
                    <h1>HarmonicAI</h1>
                    <div class="login-container"  v-if="hasAccount && !forgotPwd">
                        <div class="text-box">
                            <p>Username</p>

                            <el-input
                            v-model="username"
                            rows="1"
                            maxlength="50"
                            clearable>
                            </el-input>
                        </div>
                        <div class="text-box">
                            <p>Password</p>

                            <el-input
                            v-model="password"
                            rows="1"
                            show-password>
                            </el-input>
                        </div>
                        <div class="login-btn">
                            <button @click="showForgetPwd()">Forget your Password?</button>
                            <button class="log-in" @click="login()">Log In</button>
                        </div>

                        <div class="sign-up-option">
                            <p>Don't have an account?</p>
                            <button @click="showSignUp">Sign Up Now</button>
                        </div>
                    </div>
                    
                    <div class="sign-up-container" v-if="!hasAccount && !forgotPwd">
                        <div class="text-box">
                            <p>Username</p>

                            <el-input
                            v-model="username"
                            rows="1"
                            clearable>
                            </el-input>
                        </div>
                        <div class="text-box">
                            <p>Password</p>

                            <el-input
                            v-model="password"
                            rows="1"
                            show-password>
                            </el-input>
                        </div>
                        <div class="text-box">
                            <p>Secure Question</p>

                            <el-input
                            v-model="secure_question"
                            rows="1"
                            placeholder="Who is your most favourite artist?"
                            clearable>
                            </el-input>
                        </div>
                        <div class="signup-btn">
                            <button @click="showLogin()">Back to Log In</button>
                            <button class="sign-up" @click="createAccount()">Create Account</button>
                        </div>
                    </div>

                    <div class="forget-pwd-container" v-if="hasAccount && forgotPwd">
                        <div class="text-box">
                            <p>Username</p>
                            <div class="username">
                                <p>{{ username }}</p>
                            </div>
                        </div>
                        
                        <div class="text-box" v-if="submitSecureQuestion">
                            <p>Secure Question</p>

                            <el-input
                            v-model="secure_question"
                            rows="1"
                            placeholder="Who is your most favourite artist?"
                            clearable>
                            </el-input>
                        </div>

                        <div class="text-box" v-if="resetPwd">
                            <p>Reset Password</p>

                            <el-input
                            v-model="password"
                            rows="1"
                            clearable>
                            </el-input>
                        </div>

                        <div class="submit-btn">
                            <button @click="showLogin()">Back to Log In</button>
                            <button v-if="submitSecureQuestion" @click="ableResetPassword()" class="reset">Submit</button>
                            <button v-if="resetPwd" @click="resetPassword()" class="reset">Reset Password</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="profile-container" v-if="isLogin">
            <div class="profile-container-left">
                <div class="user-info">
                    <img :src="profile_img" />
                    <h2>{{ user_info.username }}</h2>
                    <button @click="showFullProfile(true)">Edit profile</button>
                </div>
                <div class="playlist">
                    <div class="playlist-header">
                        <h2>Playlists</h2>
                        <img 
                        v-show="!isHovered && !isEditPlaylist" 
                        @mouseover="toggleHover(true)" 
                        @mouseleave="toggleHover(false)" 
                        src="@/assets/images/icon/icon-edit.png" 
                        alt="Edit Icon White" />
                        <img 
                        v-show="isHovered && !isEditPlaylist" 
                        @mouseover="toggleHover(true)" 
                        @mouseleave="toggleHover(false)" 
                        @click="editPlaylist(true)"
                        src="@/assets/images/icon/icon-edit-blue.png" 
                        alt="Edit Icon Blue" />
                        <div class="action-btn" v-if="isEditPlaylist">
                            <h3 class="cancel" @click="editPlaylist(false)">Cancel</h3>
                        </div>
                    </div>
                    <div class="playlist-body" v-if="!isEditPlaylist">
                        <div 
                            @click="viewFullPlaylist(playlist)" 
                            class="playlist-item" 
                            v-for="playlist, index in user_info.playlist" :key="index"
                            :class="{ 'selected': selected_playlist && selected_playlist.playlist_name === playlist.playlist_name }">
                            <img :src="require(`@/assets/images/${playlist.playlist_cover}`)" />
                            <div class="playlist-details">
                                <h3>{{ playlist.playlist_name }}</h3>
                                <p>{{ playlist.song_list.length + ' songs' }}</p>
                            </div>
                        </div>
                        <div class="playlist-item-add" @click="addNewPlaylist">
                            <img class="add" src="@/assets/images/icon/icon-add.svg"/>
                            <h5>Add Playlist</h5>
                        </div>
                    </div>

                    <div class="playlist-body-edit" v-if="isEditPlaylist">
                        <div 
                            class="playlist-item" 
                            v-for="playlist, index in user_info.playlist" :key="index">
                            <img :src="require(`@/assets/images/${playlist.playlist_cover}`)" />
                            <div class="playlist-details">
                                <h3>{{ playlist.playlist_name }}</h3>
                                <p>{{ playlist.song_list.length + ' songs' }}</p>
                            </div>
                            <img class="delete" src="@/assets/images/icon/icon-delete.png"/>
                        </div>
                    </div>
                </div>
            </div>
            <div class="profile-container-right" v-if="isShowFullProfile">
                <h2>Profile</h2>
                <div class="change-info">
                    <h3>Username</h3>
                    <div class="input-container">
                        <el-input 
                            :placeholder="user_info.username"
                            v-model="username"
                            rows="1"
                            disabled
                            v-if="!isEditUsername" />
                        <el-input 
                            v-model="username"
                            rows="1"
                            v-if="isEditUsername" />
                        <button v-if="!isEditUsername" class="edit" @click="editUsername(true)">Edit</button>
                        <button v-if="isEditUsername" class="save" @click="updateUsername()">Save</button>
                        <button v-if="isEditUsername" class="cancel" @click="editUsername(false)">Cancel</button>
                    </div>
                </div>
                <div class="change-info">
                    <h3>Password</h3>
                    <div class="input-container">
                        <el-input 
                            :placeholder="user_info.password"
                            disabled
                            rows="1"
                            v-model="password"
                            v-if="!isEditPassword"/>

                        <el-input 
                        rows="1"
                        v-model="password"
                        v-if="isEditPassword"/>
                        <button v-if="!isEditPassword" class="edit" @click="editPassword(true)">Edit</button>
                        <button v-if="isEditPassword" class="save" @click="updatePassword()">Save</button>
                        <button v-if="isEditPassword" class="cancel" @click="editPassword(false)">Cancel</button>
                    </div>
                </div>
                <div class="change-info" v-if="isEditPassword">
                    <h3>Secure Question</h3>
                    <p>Who is your most favourite artist?</p>
                    <div class="input-container">
                        <el-input
                            v-model="secure_question"
                            rows="1" />
                    </div>
                </div>
                <div class="change-info-picture">
                    <h3>Profile Picture</h3>
                    <div class="upload-image">
                        <img :src="imageUrl"/>
                        <el-upload
                            class="avatar-uploader"
                            :show-file-list="false"
                            :on-success="handleAvatarSuccess"
                            :before-upload="beforeAvatarUpload"
                            drag
                            :action="`http://127.0.0.1:8000/update_profile_picture?username=${user_info.username}`"
                        >
                            
                            <div class="el-upload__text">
                                <el-icon class="avatar-uploader-icon"><upload-filled /></el-icon>
                                <div class="text">
                                    <p class="blue">Drop file here</p>
                                    <p>&nbsp;or&nbsp;</p>
                                    <p>click to upload</p>
                                </div>
                            </div>
                        </el-upload>
                    </div>
                </div>
            </div>

            <div class="profile-container-right playlist" v-if="!isShowFullProfile">
                <h2>Playlist Management</h2>
                <div class="change-info-picture">
                    <h3>Playlist Cover</h3>
                    <div class="upload-image">
                        <img v-if="coverUrl" :src="coverUrl"/>
                        <div class="no-cover" v-if="!coverUrl"/>
                        <el-upload
                            class="avatar-uploader"
                            :show-file-list="false"
                            :on-success="handleCoverSuccess"
                            :before-upload="beforeCoverUpload"
                            drag
                            :action="`http://127.0.0.1:8000/update_album_picture?username=${user_info.username}&selected_playlist=${selected_playlist.playlist_name}`"
                        >
                            
                            <div class="el-upload__text">
                                <el-icon class="avatar-uploader-icon"><upload-filled /></el-icon>
                                <div class="text">
                                    <p class="blue">Drop file here</p>
                                    <p>&nbsp;or&nbsp;</p>
                                    <p>click to upload</p>
                                </div>
                            </div>
                        </el-upload>
                    </div>
                </div>
                <div class="change-info">
                    <h3>Playlist name</h3>
                    <div class="input-container">
                        <el-input 
                            :placeholder="selected_playlist.playlist_name"
                            disabled
                            rows="1"
                            v-model="playlist_name"
                            v-if="!isEditPlaylistName"/>

                        <el-input 
                        rows="1"
                        v-model="playlist_name"
                        v-if="isEditPlaylistName"/>
                        <button v-if="!isEditPlaylistName" class="edit" @click="editPlaylistName(true)">Edit</button>
                        <button v-if="isEditPlaylistName" class="save" @click="updatePlaylistName()">Save</button>
                        <button v-if="isEditPlaylistName" class="cancel" @click="editPlaylistName(false)">Cancel</button>
                    </div>
                </div>
                <div class="change-info-songlist">
                    <div class="change-info-songlist-header">
                        <h3>Songs</h3> 
                        <div class="action-btn">
                            <button v-if="!isEditSongList" class="edit" @click="editSongList(true)">Edit</button>
                            <button v-if="isEditSongList" class="save" @click="updateSongName()">Save</button>
                            <button v-if="isEditSongList" class="cancel" @click="editSongList(false)">Cancel</button>
                        </div>
                    </div>
                    <div class="songlist-container" v-if="!isEditSongList">
                        <div class="songlist-item"
                            v-for="song, index in selected_playlist.song_list" :key="index">
                            <div class="change-info-song">
                                <h5>{{ index+1 }}</h5>
                                <h5 class="song">{{ song.song }}</h5>
                                <h5>{{ song.duration }}</h5>
                            </div>
                        </div>
                    </div>
                    
                    <div class="songlist-container" v-if="isEditSongList">
                        <div class="songlist-item"
                            v-for="song, index in selected_playlist.song_list" :key="index">
                            <div class="change-info-song">
                                <h5>{{ index+1 }}</h5>
                                <div class="input-container">
                                    <el-input 
                                    rows="1"
                                    v-model="song_name[index]"/>
                                </div>
                                <h5>{{ song.duration }}</h5>
                                <img @click="deleteSong(song.song)" src="@/assets/images/icon/icon-delete.png"/>
                            </div>
                        </div>
                        <div class="songlist-item-add">
                            <el-upload
                                class="avatar-uploader"
                                :show-file-list="false"
                                :on-success="handleAudioSuccess"
                                :before-upload="beforeAudioUpload"
                                :action="`http://127.0.0.1:8000/upload_audio?username=${user_info.username}&selected_playlist=${selected_playlist.playlist_name}`"
                            >
                                
                                <div class="el-upload__text">
                                    <el-icon><img src="@/assets/images/icon/icon-add.svg"/></el-icon>
                                    <p>Add Song</p>
                                </div>
                            </el-upload>
                        </div>
                    
                    </div>
                    
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss">
  @import "@/assets/sass/profile.scss";
</style>

<script setup>
    import { onMounted, ref, watch} from 'vue';
    import AOS from 'aos';
    import 'aos/dist/aos.css';
    import { UploadFilled } from '@element-plus/icons-vue'

    const username = ref();
    const password = ref();
    const secure_question = ref();
    const isLogin = ref(false);
    const hasAccount = ref(true);
    const forgotPwd = ref(false);
    const resetPwd = ref(false);
    const submitSecureQuestion = ref(false);
    const user_info = ref();
    const error_msg = ref();
    const profile_img = ref();
    const selected_playlist = ref({});
    const isShowFullProfile = ref(true);
    const isHovered = ref(false);
    const isEditUsername = ref(false);
    const isEditPassword = ref(false);
    const imageUrl = ref('');
    const coverUrl = ref('');
    const cover_img = ref('');
    const isEditPlaylistName = ref(false);
    const playlist_name = ref();
    const song_name = ref([]);
    const isEditSongList = ref(false);
    const isEditPlaylist = ref(false);
    const success_msg = ref();

    const updateUsername = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/update_username`, {
                method: 'PUT',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    old_username: user_info.value.username,
                    new_username: username.value
                })
            });
            if (!response.ok) {
                if(response.status === 404){
                    error_msg.value = 'User not found.';
                }
                if(response.status === 401){
                    error_msg.value = 'Username has been used.';
                }
                if(response.status === 402){
                    error_msg.value = 'Username cannot be same.';
                }
            }

            if(response.ok){
                password.value = user_info.value.password;
                getProfile();
                isEditUsername.value = false;
            }
            


        } catch (error) {
            if (error.response) {
                error_msg.value = error.response.data.detail;
            } else {
                error_msg.value = 'An error occurred';
            }
        }

        setTimeout(() => {
                error_msg.value = '';
            }, 5000);
    }

    const updatePassword = async () => {
        if (secure_question.value){
            if(secure_question.value == user_info.value.secure_question){
                try {
                    const response = await fetch(`http://127.0.0.1:8000/update_password`, {
                        method: 'PUT',
                        headers: {
                        'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            username: user_info.value.username,
                            new_password: password.value
                        })
                    });
                    if (!response.ok) {
                        if(response.status === 404){
                            error_msg.value = 'User not found.';
                        }
                    }

                    if(response.ok){
                        username.value = user_info.value.username;
                        getProfile();
                        isEditPassword.value = false;
                    }

                    

                } catch (error) {
                    if (error.response) {
                        error_msg.value = error.response.data.detail;
                    } else {
                        error_msg.value = 'An error occurred';
                    }
                }
            }
            else{
                error_msg.value = "The answer doesn't match."
            }
        }
        else{
            error_msg.value = "Please fill in the secure question."
        }

        setTimeout(() => {
                error_msg.value = '';
            }, 5000);
    }

    const updatePlaylistName = async() => {
        if(playlist_name.value != selected_playlist.value.playlist_name){
            try {
                const response = await fetch(`http://127.0.0.1:8000/update_playlist_name`, {
                    method: 'PUT',
                    headers: {
                    'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: user_info.value.username,
                        old_playlist_name: selected_playlist.value.playlist_name,
                        new_playlist_name: playlist_name.value
                    })
                });
                if (!response.ok) {
                    if(response.status === 404){
                        error_msg.value = 'User not found.';
                    }
                    if(response.status === 402){
                        error_msg.value = 'Playlist name already exists.';
                    }
                    if(response.status === 400){
                        error_msg.value = 'Playlist name cannot be the same.';
                    }
                }

                if(response.ok){
                    username.value = user_info.value.username;
                    password.value = user_info.value.password;
                    success_msg.value = "Playlist name changed successfully.";
                    getProfile();
                    isEditPlaylistName.value = false;
                    selected_playlist.value = user_info.value.playlist.find(playlist => playlist.playlist_name === selected_playlist.value.playlist_name);
                }

            } catch (error) {
                if (error.response) {
                    error_msg.value = error.response.data.detail;
                } else {
                    error_msg.value = 'An error occurred';
                }
            }
        }

        else{
            error_msg.value = "Playlist name cannot be the same.";
        }
    }

    const updateSongName = async() => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/update_song_name`, {
                method: 'PUT',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: user_info.value.username,
                    selected_playlist: selected_playlist.value.playlist_name,
                    song_name_list: song_name.value
                })
            });
            if (!response.ok) {
                if(response.status === 404){
                    error_msg.value = 'User not found.';
                }
                if(response.status === 401){
                    error_msg.value = 'Playlist not found.';
                }
                if(response.status === 400){
                    error_msg.value = 'The number of new song names must match the number of existing songs in the playlist.';
                }
            }

            if(response.ok){
                username.value = user_info.value.username;
                password.value = user_info.value.password;
                success_msg.value = "Song names updated successfully.";
                await getProfile();
                editSongList(false);
                selected_playlist.value = user_info.value.playlist.find(playlist => playlist.playlist_name === selected_playlist.value.playlist_name);
            }

        } catch (error) {
            if (error.response) {
                error_msg.value = error.response.data.detail;
            } else {
                error_msg.value = 'An error occurred';
            }
        }
    }

    const addNewPlaylist = async() => {
        isShowFullProfile.value = false;
        try {
            const response = await fetch(`http://127.0.0.1:8000/create_playlist?username=${user_info.value.username}`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
                }
            });
            if (!response.ok) {
                error_msg.value = 'Failed to create playlist.';
            }

            if(response.ok){
                username.value = user_info.value.username;
                password.value = user_info.value.password;
                await getProfile();
                selected_playlist.value = user_info.value.playlist[user_info.value.playlist.length - 1];
            }

        } catch (error) {
            if (error.response) {
                error_msg.value = error.response.data.detail;
            } else {
                error_msg.value = 'An error occurred';
            }
        }
    }

    const deleteSong = async(song) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/delete_song`, {
                method: 'PUT',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: user_info.value.username,
                    selected_playlist: selected_playlist.value.playlist_name,
                    song_name: song
                })
            });
            if (!response.ok) {
                if(response.status === 404){
                    error_msg.value = 'User not found.';
                }
                if(response.status === 401){
                    error_msg.value = 'Playlist not found.';
                }
                if(response.status === 400){
                    error_msg.value = 'Song removed unsuccessfully.';
                }
            }

            if(response.ok){
                username.value = user_info.value.username;
                password.value = user_info.value.password;
                success_msg.value = "Song removed successfully.";
                await getProfile();
                selected_playlist.value = user_info.value.playlist.find(playlist => playlist.playlist_name === selected_playlist.value.playlist_name);
            }

        } catch (error) {
            if (error.response) {
                error_msg.value = error.response.data.detail;
            } else {
                error_msg.value = 'An error occurred';
            }
        }
    }

    const editPlaylist = (bool) => {
        isEditPlaylist.value = bool;
    }

    const editUsername = (bool) => {
        isEditUsername.value = bool;
        username.value = user_info.value.username;
    }

    const editPassword = (bool) => {
        isEditPassword.value = bool;
        password.value = user_info.value.password;
    }

    const editPlaylistName = (bool) => {
        isEditPlaylistName.value = bool;
        playlist_name.value = selected_playlist.value.playlist_name;
    }

    const editSongList = (bool) => {
        isEditSongList.value = bool;
        selected_playlist.value.song_list.forEach((song, index) => {
            song_name.value[index] = song.song;
        });
    }

    const handleAvatarSuccess = (response, uploadFile) => {
        if (uploadFile.raw) {
            imageUrl.value = URL.createObjectURL(uploadFile.raw)
        }
        
        username.value = user_info.value.username;
        password.value = user_info.value.password;
        getProfile();
    }

    const beforeAvatarUpload = (rawFile) => {
        if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png' ) {
            error_msg.value = 'Cover picture must be JPG/PNG format!';
            setTimeout(() => {
                error_msg.value = '';
            }, 5000);
            return false
        } 
        return true
    }

    const handleCoverSuccess = (response, uploadFile) => {
        if (uploadFile.raw) {
            coverUrl.value = URL.createObjectURL(uploadFile.raw)
        }

        username.value = user_info.value.username;
        password.value = user_info.value.password;
        getProfile();
    }

    const beforeCoverUpload = (rawFile) => {
        if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png' ) {
            error_msg.value = 'Cover picture must be JPG/PNG format!'
            setTimeout(() => {
                error_msg.value = '';
            }, 5000);
            return false
        } 
        return true
    }

    const handleAudioSuccess = async(response, uploadFile) => {
        if (uploadFile.raw) {
            username.value = user_info.value.username;
            password.value = user_info.value.password;
            await getProfile();
            selected_playlist.value = user_info.value.playlist.find(playlist => playlist.playlist_name === selected_playlist.value.playlist_name);            
            isEditSongList.value = false;
        }
    }

    const beforeAudioUpload = (rawFile) => {
        const fileType = rawFile.type;
        if (!fileType || !fileType.startsWith('audio/')) {
            error_msg.value = 'Audio file must be MP3/WAV format!'
            setTimeout(() => {
                error_msg.value = '';
            }, 5000);
            return false
        } 
        return true
    }

    const showFullProfile = (bool) => {
        isShowFullProfile.value = bool;
        selected_playlist.value = null;
    }

    const toggleHover = (bool) => {
        isHovered.value = bool;
    }

    const showSignUp = () => {
        hasAccount.value = false;
        username.value = '';
        password.value = '';
        secure_question.value = '';
    }

    const showLogin = () => {
        hasAccount.value = true;
        forgotPwd.value = false;
        resetPwd.value = false;
        submitSecureQuestion.value = false;
        username.value = '';
        password.value = '';
        secure_question.value = '';
    }

    const showForgetPwd = () => {
        if(username.value){
            forgotPwd.value = true;
            submitSecureQuestion.value = true;
        }

        else{
            error_msg.value = 'Please enter your username.';
        }
        
    }

    const ableResetPassword = async() => {
        if(secure_question.value){
            try{
                const response = await fetch(`http://127.0.0.1:8000/check_secure_question`, {
                    method: 'POST',
                    headers:{'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        username: username.value,
                        secure_question: secure_question.value
                    })
                });

                if (!response.ok) {
                    if(response.status === 401){
                        error_msg.value = "Secure question doesn't match.";
                    }
                    if(response.status === 404){
                        error_msg.value = "User not found.";
                    }
                }

                if(response.ok){
                    resetPwd.value = true;
                    submitSecureQuestion.value = false;
                }
            }

            catch(error){
                if (error.response) {
                    error_msg.value = error.response.data.detail;
                }
            }
        }
        
        else{
            error_msg.value = 'Please enter secure question.';
        }
    }

    const resetPassword = async() => {
        if(username.value && password.value && secure_question.value){
            try{
                const response = await fetch(`http://127.0.0.1:8000/update_password`, {
                    method: 'PUT',
                    headers:{'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        username: username.value,
                        new_password: password.value
                    })
                });

                if (!response.ok) {
                    if(response.status === 404){
                        error_msg.value = "User not found.";
                    }
                }

                if(response.ok){
                    hasAccount.value = true;
                    forgotPwd.value = false;
                    resetPwd.value = false;
                    submitSecureQuestion.value = false;
                    username.value = '';
                    password.value = '';
                    secure_question.value = '';
                    success_msg.value = 'Password reset successfully.';
                }
            }

            catch(error){
                if (error.response) {
                    error_msg.value = error.response.data.detail;
                }
            }
        }
    }

    const createAccount = async() => {

        if(username.value && password.value && secure_question.value){

            try{
                const response = await fetch(`http://127.0.0.1:8000/create_account`, {
                    method: 'POST',
                    headers:{'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        username: username.value,
                        password: password.value,
                        secure_question: secure_question.value
                    })
                });

                if (!response.ok) {
                    if(response.status === 401){
                        error_msg.value = 'Username already exists.';
                    }
                }

                if(response.ok){
                    username.value = '';
                    password.value = '';
                    secure_question.value = '';
                    hasAccount.value = true;
                    forgotPwd.value = false;
                    resetPwd.value = false;
                    submitSecureQuestion.value = false;
                    success_msg.value = "User created successfully.";
                }
            }

            catch(error){
                if (error.response) {
                    error_msg.value = error.response.data.detail;
                }
            }
        }

        else{
            error_msg.value = 'All fields are required.';
        }
        
    }

    const getProfile = async() => {
        if(username.value && password.value){
            error_msg.value = '';
            try {
                const response = await fetch(`http://127.0.0.1:8000/login`, {
                    method: 'GET',
                    headers: {
                    'Content-Type': 'application/json',
                    'username': username.value,
                    'password': password.value
                    },
                });
                if (!response.ok) {
                    if(response.status === 404){
                        error_msg.value = 'Incorrect password.';
                    }
                    if(response.status === 401){
                        error_msg.value = 'User not found.';
                    }
                }

                const data = await response.json();
                user_info.value = data;

                if(response.ok){
                    const userDataJSON = JSON.stringify(user_info);
                    sessionStorage.setItem('userInfo', userDataJSON); 
                    if (user_info.value.profile_img) {
                        profile_img.value  = require(`@/assets/images/${user_info.value.profile_img}`);
                    }
                }
            } catch (error) {
                console.error('Error fetching user:', error);
            }
        }
        else{
            error_msg.value = 'Please enter your username and password.';
        }
        setTimeout(() => {
            error_msg.value = '';
        }, 5000);
    }

    const login = async() => {
        await getProfile();
        if(user_info.value != null){
            isLogin.value = true;
        }
    }

    const viewFullPlaylist = (playlist) => {
        selected_playlist.value = playlist;
        isShowFullProfile.value = false;
        coverUrl.value = require(`@/assets/images/${selected_playlist.value.playlist_cover}`);
        cover_img.value = require(`@/assets/images/${selected_playlist.value.playlist_cover}`);
    }

    onMounted(() => {
        AOS.init({
        duration: 1800,
        });

        // Retrieve user information JSON string from session storage
        const userDataJSON = sessionStorage.getItem('userInfo');

        if(userDataJSON != null){
            // Parse JSON string back into an object
            const userData = JSON.parse(userDataJSON);
            user_info.value = userData._rawValue;

            if(user_info.value != {}){
                isLogin.value = true;
                if (user_info.value.profile_img) {
                    imageUrl.value  = require(`@/assets/images/${user_info.value.profile_img}`);
                    profile_img.value  = require(`@/assets/images/${user_info.value.profile_img}`);
                }
            }
            else{
                isLogin.value = false;
            }
        }
    });

    watch(error_msg, (newValue) => {
        if (newValue) {
            success_msg.value = '';
            setTimeout(() => {
                error_msg.value = '';
            }, 5000);}
    });

    watch(success_msg, (newValue) => {
        if (newValue) {
            error_msg.value = '';
            setTimeout(() => {
                success_msg.value = '';
            }, 5000);
        }
    });
</script>