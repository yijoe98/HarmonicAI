Requirements:
1. Node.js
   a. To download the Node.js, https://nodejs.org/en
   b. Check node.js version in command prompt, use command 'npm -v'.
2. Python 
   a. To download python, https://www.python.org/downloads/
   b. Check python version in command prompt, use command 'python3 --version'.
3. Python's package installer (pip)
   a. To check pip installation, use command 'pip -V'.
4. FastAPI
   a. To download FastAPI, use command 'pip install fastapi uvicorn'.
5. PyTorch
   a. To download PyTorch, use command "python -m pip install 'torch==2.1.0'".
6. Audiocraft model
   a. To download the model, use command 'python -m pip install -U audiocraft'.
7. Transformer
   a. To install transformer library, use command 'pip install git+https://github.com/huggingface/transformers.git'.
8. MongoDB
    a. To install mongoDB, https://www.mongodb.com/try/download/shell
    b. Manual of mongoDB, https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/
    c. To download mongoDB Compass (GUI), https://www.mongodb.com/try/download/compass

-------------------------------------------------------------------------------------------
1. To download the images, videos, and audios, go to this path: harmonicai/frontend/src/assets/
2. To download the databases, go to: harmonicai/backend/database/

-------------------------------------------------------------------------------------------
Database preparation:
1. Run MongoDB Compass
2. Connect to mongoDB deployment:
    a. Click 'connect' with default URI: mongodb://localhost:27017
    b. Create a new database and rename it as 'HarmonicAI' 
    c. Create four collections which name as 'genre_playlist', 'music_data', 'music_description', and 'user_data'
    d. The name of database and collections must be the same mentioned above.
    e. For each collection, import the JSON data from '/harmonicai/backend/database/HarmonicAI.{collection_name}'

-------------------------------------------------------------------------------------------
To run the application successfully:
1. Download and unzip the whole harmonicai folder.
2. Open a new terminal.
3. Direct to the path 'path_to_the_folder/harmonicai/frontend'.
4. Run 'npm install' command and it will start downloading necessary package.
5. Run ' npm run serve' command and click on the link to launch the frontend of the application.
6. Open another new terminal.
7. Direct to the path 'path_to_the_folder/harmonicai/backend/app'.
8. Run 'uvicorn api:app --reload' command to lauch the backend of the application.
9. Now, you should be able to see a website that is connected to an API open in your browser.

--------------------------------------------------------------------------------------------

Model:
https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md
