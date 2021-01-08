# Simple Bulletin Board and Multimedia Streaming

A coursework in NTU Computer Network 2020Fall.

## Description
A simple webpage which provides bulletin board, automatic speech recognition (ASR) service and video streaming/sharing.
Implemented with basic socket programming in python and simple HTML.

## Getting Started

### Dependency
Use `pip install -r requirements.txt` to install required package.
- Note that `deepspeech_pytorch` may need manual installation. Check [here](https://github.com/SeanNaren/deepspeech.pytorch) for more information

### Execution
```bash
python bulletin_server.py [-p PORT_NUM]
python asr_server.py [-p PORT_NUM]
python video_server.py [-p PORT_NUM]
```

- By default, all the service runs with port number `9527`.
- In `templates/index.html`, the link to other application (asr/video streaming) is hard-coded to my workstation ip with port number `9528` and `9529`. You need modify them when deploying this code on your machine.
