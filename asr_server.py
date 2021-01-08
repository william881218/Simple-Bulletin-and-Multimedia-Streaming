import random
import os
from argparse import ArgumentParser

from flask import Flask, request, jsonify, render_template, send_file
import logging
from scipy.io import wavfile
import numpy as np

from art.estimators.speech_recognition.pytorch_deep_speech import PyTorchDeepSpeech


# instantiate flask app
app = Flask(__name__)

app.config['ROOT_DIR'] = ROOT_DIR = os.path.dirname(__file__)
app.config['UPLOAD_DIR'] = os.path.join(ROOT_DIR, 'upload') # for uploaded files
app.config['AUDIO_DIR'] = os.path.join(ROOT_DIR, 'output') # for generated files
app.config['OUTPUT_PATH'] = os.path.join(app.config['AUDIO_DIR'], 'perturbed.wav')

# create video directory
try:  
    os.mkdir('upload')  
except OSError as error:  
    pass


@app.route('/', methods=['GET'])
def main_page():
    '''
    Return the main page.
    '''
    return render_template('asr.html')


@app.route('/corpus/7.wav', methods=['GET'])
def download_corpus():
    '''
    Responsible for downloading audio corpuses. 
    Currently only 7.wav is available.
    '''
    return send_file(os.path.join(app.config["ROOT_DIR"], "corpus/7.wav"), as_attachment=True)


@app.route("/asr", methods=["POST"])
def asr():
    """Endpoint to use asr
    :return (json): This endpoint returns a json file with the following format:
        {
            "transcription": TRANSCRIPTION
        }
    """
    
    # prepare the path where the uploaded/generated audio are saved
    file_idx = str(random.randint(0, 100000)) + '.wav'
    uploaded_path = os.path.join(app.config['UPLOAD_DIR'], file_idx)
    output_path = os.path.join(app.config['AUDIO_DIR'], file_idx)

    # get file from POST request and save it
    audio_file = request.files["file"]
    audio_file.save(uploaded_path)
    logging.info("File saved at {}".format(uploaded_path))


    asr_model = PyTorchDeepSpeech(pretrained_model="librispeech",
                                  device_type="cpu")

    # load audio
    sample_rate, sound = wavfile.read(uploaded_path)

    if sample_rate != 16000: # check if it has valid sample rate
        transcription = "SAMPLE_RATE_ERROR"
        logging.info("Sample rate error.")
    else: # start prediction
        transcription = asr_model.predict(np.array([sound]), batch_size=1,transcription_output=True)[0]
        logging.info("Finish prediction. Transcription: {}".format(transcription))
    
    # we don't need the audio file any more - let's delete it!
    os.remove(uploaded_path)

    # send back html page with result
    transcription = {"text": transcription}
    return render_template('transcription.html', transcription=transcription)


if __name__ == "__main__":

    # handle arg parser
    argparse = ArgumentParser()
    argparse.add_argument('-p', '--port', type=int, default=9527)
    args = argparse.parse_args()

    app.run(debug=True, host='0.0.0.0', port=args.port)