import random
import os

import cv2
from flask import Flask, request, render_template, send_file, Response
import logging


# instantiate flask app
app = Flask(__name__)

app.config['ROOT_DIR'] = ROOT_DIR = os.path.dirname(__file__)
app.config['VIDEO_PATH'] = 'video/video.mp4'
app.config['VIDEO_NAME'] = "海洋科學概論課堂影片 - 離暗流之危險"

# create video directory
try:  
    os.mkdir('video')  
except OSError as error:  
    pass


@app.route('/', methods=['GET'])
def main_page():
    '''
    Return the main page.
    '''
    return render_template('video.html', video_name=app.config['VIDEO_NAME'])


# for streaming
@app.route('/video_streaming')
def video_streaming():
    '''
    Streaming video.
    '''
    # define a generator that yield each frame
    def video_generator():
        cap = cv2.VideoCapture(app.config['VIDEO_PATH'])
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            else:
                # shape = frame.shape # H x W x C
                # new_h = int(720 / shape[1] * shape[0])
                # frame = cv2.resize(frame, (new_h, 720, 3))
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(video_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/download', methods=['GET'])
def download_perturbed_audio():
    '''
    Download the perturbed audio.
    Note that every time a perturbed audio is generated,
    the old one on server will be replaced.
    '''
    return send_file(app.config['VIDEO_PATH'], as_attachment=True)


@app.route("/upload", methods=["POST"])
def upload():
    """
    Upload new video.
    """

    # get file from POST request and save it
    audio_file = request.files["file"]
    audio_file.save(app.config['VIDEO_PATH'])

    # get target from POST request
    app.config['VIDEO_NAME'] = request.form["name"]

    # send back html page with result
    return render_template('video.html', video_name=app.config['VIDEO_NAME'])



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='9527')