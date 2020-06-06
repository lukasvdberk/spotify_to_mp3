### About
This is a small script to download your spotify playlist as a mp3. It does this by getting your spotify playlist data and then search it up on youtube. 
### Installation
requirements
1. python3
2. pip3
3. ffmpeg

Install ffmpeg

On debian based systems.
```bash
sudo apt install ffmpeg
```

To install all the requirements for this project
```bash
pip install -r requirements.txt
```

Fill in the variables in the example-env file.
Client id and secret come from the spotify api. 
Make sure when creating an application on the spotify developer platform that redirect url is http://locahost:8080

After that you can run it
```bash
source .example-env && python3 app.py
```
