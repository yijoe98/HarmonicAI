from fastapi import FastAPI, Response, Query, HTTPException, Header, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Dict
from datetime import datetime
import json
from json import dumps, loads
import pandas as pd
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import gensim.downloader as api
from gensim.parsing.preprocessing import remove_stopwords
import os
import shutil
from transformers import pipeline
import scipy
from pydub import AudioSegment
from pydub.utils import mediainfo
import pytz

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client.HarmonicAI
genre_playlist = db.genre_playlist
music_data = db.music_data
user_data = db.user_data
music_description = db.music_description


model = api.load('word2vec-google-news-300')
songs = pd.read_csv('../database/cleaned_spotify_songs.csv')
song_vector = np.load('../database/song_vector.npy')
artists_vector = np.load('../database/artists_vector.npy')
genres_vector = np.load('../database/genres_vector.npy')
song_names = songs["track_name"]
artist = songs["track_artist"]
track_id = songs["track_id"]
duration = songs["duration"]
genre = songs["genre"]
listen_count = songs["listen_count"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

GMT8 = pytz.timezone('Asia/Shanghai')

IMAGE_DIRECTORY = "C:/Users/user/Desktop/FYP/harmonicai/frontend/src/assets/images"
AUDIO_DIRECTORY = "C:/Users/user/Desktop/FYP/harmonicai/frontend/src/assets/audio"

if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

if not os.path.exists(AUDIO_DIRECTORY):
    os.makedirs(AUDIO_DIRECTORY)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime)):
        return obj.isoformat()
    raise TypeError("Type not serializable")

class UserInput(BaseModel):
    text: str

class UpdateHistoryRequest(BaseModel):
    username: str
    history: List[str]

class UpdateUsernameRequest(BaseModel):
    old_username: str
    new_username: str

class UpdatePasswordRequest(BaseModel):
    username: str
    new_password: str

class UserInfo(BaseModel):
    username: str
    password: str

class Playlist(BaseModel):
    playlist_name: str
    song_list: List[str]
    playlist_cover: str

class MusicDescription(BaseModel):
    genre: str
    mood: str

class Item(BaseModel):
    music_desc: str

class CreateAccountRequest(BaseModel):
    username: str
    password: str
    secure_question: str

class CheckSecureQuestion(BaseModel):
    username: str
    secure_question: str

class UpdatePlaylistNameRequest(BaseModel):
    username: str
    old_playlist_name: str
    new_playlist_name: str

class UpdateSongNameRequest(BaseModel):
    username: str
    selected_playlist: str
    song_name_list: List[str]

class RemoveSongRequest(BaseModel):
    username: str
    selected_playlist: str
    song_name: str

class UpdateListenCountRequest(BaseModel):
    track_id: str

@app.post("/generate_audio")
async def generate_audio(item: Item):
    try:
        synthesiser = pipeline("text-to-audio", "facebook/musicgen-small", model_kwargs={"max_length": 1500})

        music = synthesiser(item.music_desc, forward_params={"do_sample": True})

        audio_io = io.BytesIO()
        scipy.io.wavfile.write(audio_io, rate=music["sampling_rate"], data=music["audio"])

        response = Response(content=audio_io.getvalue())
        response.headers["Content-Disposition"] = f'attachment; filename="{item.music_desc}.wav"'
        response.headers["Content-Type"] = 'audio/wav'

        return response
    except Exception as e:
        return {"error": str(e)}

@app.get("/genre_playlist", response_model=List[Dict[str, str]])
async def get_genre_playlist(genre: str = Query(None, description="Filter songs by genre")):
    try:
        query = {} if not genre else {"genre": genre}
        playlist = list(genre_playlist.find(query, {"_id": 0}))  # Exclude _id field from response
        
        # Serialize the playlist with datetime objects handled
        serialized_playlist = json.loads(json.dumps(playlist, default=json_serial))

        return JSONResponse(content=serialized_playlist)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/popular_song")
async def get_popular_songlist():
    try:
        popular_songs = list(music_data.find({}, {"_id": 0}).sort("listen_count", -1).limit(50)) 
        popular_songs = json.loads(json.dumps(popular_songs, default=json_serial))
        return JSONResponse(content=popular_songs)  # Deserialize for JSONResponse
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/popular_artist")
async def get_popular_artist():
    try:
        songs_cursor = music_data.find({}, {"_id": 0, "track_artist": 1, "listen_count": 1})
        songs_list = list(songs_cursor)
        
        songs_df = pd.DataFrame(songs_list)
        
        artist_listen_count = songs_df.groupby('track_artist')['listen_count'].sum()
        
        artist = artist_listen_count.sort_values(ascending=False).head(3)
        
        artist = artist.reset_index()
        
        popular_artist = artist.to_dict(orient='records')
        
        serialized_popular_artist = json.loads(json.dumps(popular_artist))
        
        return JSONResponse(content=serialized_popular_artist)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/artist_playlist", response_model=List[Dict[str, str]])
async def get_artist_playlist(artist: str = Query(None, description="Filter songs by artist")):
    try:
        # Define query based on artist parameter
        query = {} if not artist else {"track_artist": artist}
        
        # Retrieve artist's playlist from MongoDB and sort by listen_count
        artist_playlist = list(music_data.find(query, {"_id": 0}).sort("listen_count", -1))
        
        # Serialize playlist to JSON
        serialized_playlist = json.loads(json.dumps(artist_playlist, default=json_serial))
        
        # Return JSON response
        return JSONResponse(content=serialized_playlist)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/login")
async def login_user(username: str = Header(...), password: str = Header(...)):

    db_user = user_data.find_one({"username": username}, {"_id": 0})
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")
    if password != db_user['password']:
        raise HTTPException(status_code=404, detail='Incorrect password.')
    
    return db_user

@app.post("/recommendation")
async def find_similar_songs(user_input: UserInput):

    def sentence_vector(sentence, model):
        words = [word for word in sentence if word in model]
        if not words:
            return np.zeros(model.vector_size)
        return np.mean([model[word] for word in words], axis=0)
    
    input_sentence_processed = remove_stopwords(user_input.text.lower()).split()
    input_sentence_vector = sentence_vector(input_sentence_processed, model)

    name_similarities = cosine_similarity([input_sentence_vector], song_vector).flatten()
    genre_similarities = cosine_similarity([input_sentence_vector], genres_vector).flatten()
    artist_similarities = cosine_similarity([input_sentence_vector], artists_vector).flatten()

    weight_genre = 0.2
    weight_artist = 0.2
    weight_name = 0.6

    combined_similarities = (weight_name * name_similarities) + (weight_genre * genre_similarities) + (weight_artist * artist_similarities)

    top_indices = combined_similarities.argsort()[-10:][::-1]
    similar_songs = [{"song_names": song_names[idx],
                      "track_id": track_id[idx], 
                      "artist": artist[idx],
                      "genre": genre[idx],
                      "duration": duration[idx],
                      "listen_count": int(listen_count[idx]),
                      "similarity": combined_similarities[idx], 
                      } for idx in top_indices]
    return similar_songs

@app.post("/update_listening_history")
async def update_listening_history(request: UpdateHistoryRequest):
    username = request.username
    history = request.history

    user = user_data.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the listening history
    user_data.update_one(
        {"username": username},
        {"$set": {"history": history}}
    )

    return {"status": "success"}

@app.post("/update_profile_picture")
async def update_profile_picture(username: str, file: UploadFile = File(...)):

    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    user = user_data.find_one({"username": username})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Save the uploaded file to the specified directory
    file_location = os.path.join(IMAGE_DIRECTORY, file.filename)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update the user document in MongoDB with the relative path to the file
    update_result = user_data.update_one(
        {"username": username},
        {"$set": {"profile_img": file.filename}}
    )

    if update_result.modified_count == 1:
        return JSONResponse(status_code=200, content={"msg": "Profile picture updated successfully"})
    else:
        raise HTTPException(status_code=500, detail="Failed to update profile picture")

@app.post("/update_album_picture")
async def update_album_picture(username: str, selected_playlist: str, file: UploadFile = File(...)):

    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    user_playlist = user_data.find_one({"username": username, "playlist.playlist_name": selected_playlist})

    if user_playlist is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Save the uploaded file to the specified directory
    file_location = os.path.join(IMAGE_DIRECTORY, file.filename)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update the user document in MongoDB with the relative path to the file
    update_result = user_data.update_one(
        {"username": username, "playlist.playlist_name": selected_playlist},
        {"$set": {"playlist.$.playlist_cover": file.filename}}
    )

    if update_result.modified_count == 1:
        return JSONResponse(status_code=200, content={"msg": "Profile picture updated successfully"})
    else:
        raise HTTPException(status_code=500, detail="Failed to update profile picture")

@app.put("/update_username")
async def update_username(request: UpdateUsernameRequest):
    user = user_data.find_one({"username": request.old_username})
    new_username = user_data.find_one({"username": request.new_username})

    if request.old_username == request.new_username:
        raise HTTPException(status_code=402, detail="Username cannot be same")
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if new_username is None:
        update_result = user_data.update_one(
            {"username": request.old_username},
            {"$set": {"username": request.new_username}}
        )
    if new_username:
        raise HTTPException(status_code=401, detail="Username has been used.")

    if update_result.modified_count == 1:
        return {"msg": "Username updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update username")
    
@app.put("/update_password")
async def update_password(request: UpdatePasswordRequest):
    user = user_data.find_one({"username": request.username})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_result = user_data.update_one(
        {"username": request.username},
        {"$set": {"password": request.new_password}}
    )

    if update_result.modified_count == 1:
        return {"msg": "Password updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update password")

@app.post("/create_playlist")
async def create_playlist(username: str):
    user = user_data.find_one({"username": username})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    current_date = datetime.now(GMT8).isoformat()

    playlist_length = len(user.get("playlist", []))
    new_playlist_name = f"Playlist {playlist_length + 1}"

    new_playlist = {
        "playlist_name": new_playlist_name,
        "song_list": [],
        "date_created": current_date,
        "playlist_cover": ''
    }
    update_result = user_data.update_one(
        {"username": username},
        {"$push": {"playlist": new_playlist}},
    )

    if update_result.modified_count == 1:
        return {"msg": "Playlist created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to create playlist")

@app.put("/delete_song")
async def delete_song(request: RemoveSongRequest):
    user = user_data.find_one({"username": request.username})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_playlist = next((playlist for playlist in user.get('playlist', []) if playlist['playlist_name'] == request.selected_playlist), None)
    
    if not existing_playlist:
        raise HTTPException(status_code=401, detail="Playlist not found.")

    updated_song_list = [song for song in existing_playlist.get('song_list', []) if str(song.get('song')) != request.song_name]
    
     # Update the playlist in the user document
    result = user_data.find_one_and_update(
        {"username": request.username, "playlist.playlist_name": request.selected_playlist},
        {"$set": {"playlist.$.song_list": updated_song_list}}
    )

    if not result:
        raise HTTPException(status_code=500, detail="Failed to update playlist")

    return {"msg": "Song removed successfully"}

@app.post("/upload_audio")
def upload_audio(username: str, selected_playlist: str, file: UploadFile = File(...)):

    user = user_data.find_one({"username": username, "playlist.playlist_name": selected_playlist})
    if user is None:
        raise HTTPException(status_code=404, detail="User or playlist not found.")

    file_location = os.path.join(AUDIO_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_date = datetime.now(GMT8).isoformat()
    audio = AudioSegment.from_file(file_location)
    duration = len(audio) / 1000.0 
    duration_minutes = int(duration // 60)
    duration_seconds_remainder = int(duration % 60)
    formatted_duration = f"{duration_minutes:02}:{duration_seconds_remainder:02}"
    new_song = {
        "song": file.filename,
        "date_created": current_date,
        "duration": formatted_duration,
        "audio_filenames": file.filename
    }
    update_result = user_data.update_one(
        {"username": username, "playlist.playlist_name": selected_playlist},
        {"$push": {"playlist.$.song_list": new_song}},
    )
    if update_result.modified_count == 1:
        return {"msg": "Song added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add song.")

@app.put("/update_playlist_name")
async def update_playlist_name(request: UpdatePlaylistNameRequest):
    if request.old_playlist_name == request.new_playlist_name:
        raise HTTPException(status_code=400, detail="Playlist names cannot be the same.")

    user = user_data.find_one({"username": request.username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    existing_playlist = user_data.find_one({"username": request.username, "playlist.playlist_name": request.new_playlist_name})
    if existing_playlist:
        raise HTTPException(status_code=402, detail="Playlist name already exists.")

    update_result = user_data.update_one(
        {"username": request.username, "playlist.playlist_name": request.old_playlist_name},
        {"$set": {"playlist.$.playlist_name": request.new_playlist_name}}
    )

    if update_result.modified_count == 1:
        return {"msg": "Playlist name changed successfully."}
    else:
        raise HTTPException(status_code=500, detail="Failed to change playlist name.")
   
@app.put("/update_song_name")
async def update_song_name(request: UpdateSongNameRequest):
    user = user_data.find_one({"username": request.username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    existing_playlist = next((playlist for playlist in user.get('playlist', []) if playlist['playlist_name'] == request.selected_playlist), None)
    
    if not existing_playlist:
        raise HTTPException(status_code=401, detail="Playlist not found.")

    current_song_list = existing_playlist.get('song_list', [])

    if len(request.song_name_list) != len(current_song_list):
        raise HTTPException(status_code=400, detail="The number of new song names must match the number of existing songs in the playlist.")

    new_song_list = [
        {**song, "song": new_name}
        for song, new_name in zip(current_song_list, request.song_name_list)
    ]

    update_result = user_data.update_one(
        {"username": request.username, "playlist.playlist_name": request.selected_playlist},
        {"$set": {"playlist.$.song_list": new_song_list}}
    )

    if update_result.modified_count == 1:
        return {"msg": "Song names updated successfully."}
    else:
        raise HTTPException(status_code=500, detail="Failed to update song names.") 

@app.post("/music_description")
async def get_music_description(description_request: MusicDescription):
    try:
        query = {}
        if description_request.genre != '':
            query["genre"] = description_request.genre
        if description_request.mood != '':
            query["mood"] = description_request.mood

        music_descriptions = list(music_description.find(query, {"_id": 0}))
        music_descriptions = json.loads(json.dumps(music_descriptions, default=json_serial))
        return JSONResponse(content=music_descriptions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/create_account")
async def create_account(create_acc: CreateAccountRequest):
    db_user = user_data.find_one({"username": create_acc.username}, {"_id": 0})
    if db_user:
        raise HTTPException(status_code=401, detail="Username already exists")
    
    if not db_user:
        new_user = {
            "username": create_acc.username,
            "password": create_acc.password,
            "secure_question": create_acc.secure_question,
            "playlist": [],
            "profile_img": '',
            "history": []
        }
        
        user_data.insert_one(new_user)
        return {"msg": "User created successfully"}
    
@app.post("/check_secure_question")
async def check_secure_question(check_sq: CheckSecureQuestion):
    user = user_data.find_one({"username": check_sq.username}, {"_id": 0})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user["secure_question"] == check_sq.secure_question:
        return {"msg": "Secure question matches"}

    if user["secure_question"] != check_sq.secure_question:
        raise HTTPException(status_code=401, detail="Secure question doesn't match.")

@app.put("/update_listen_count")
async def update_listen_count(request: UpdateListenCountRequest):
    track_id = request.track_id

    # Find the track by track_id
    track = music_data.find_one({"track_id": track_id})
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    # Increment the listen_count
    new_listen_count = track.get("listen_count", 0) + 1

    # Update the listen_count in MongoDB
    music_data.update_one(
        {"track_id": track_id},
        {"$set": {"listen_count": new_listen_count}}
    )

    return {"status": "success"}

if __name__ == "__api__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)