from flask import Flask, render_template, request
from pathlib import Path #pip install pathlib https://pypi.org/project/pathlib/
import os
import yt_dlp


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/download", methods=["GET", "POST"])
def downloadVideo():
    mesage = ''
    errorType = 0
    if request.method == 'POST' and 'video_url' in request.form:
        youtubeUrl = request.form["video_url"]
        if youtubeUrl:
            try:
                downloadFolder = str(os.path.join(Path.home(), "Downloads/"))
                
                # Añadir opción para evitar descargar listas de reproducción
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': os.path.join(downloadFolder, '%(title)s.%(ext)s'),
                    'noplaylist': True  # Esta opción evita descargar la playlist
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtubeUrl])
                
                mesage = 'Video Downloaded Successfully!'
                errorType = 1
            except Exception as e:
                mesage = f'An unexpected error occurred: {str(e)}'
                errorType = 0
        else:
            mesage = 'Enter YouTube Video Url.'
            errorType = 0
    return render_template('youtube.html', mesage=mesage, errorType=errorType)


if __name__ == "__main__":
    app.run(debug=True)