# Wyoming Whisper API client

[Wyoming protocol](https://github.com/rhasspy/wyoming) server
for theWhisper API speech to text system.

My motivation was to establish a one working STT system for whole
household, additionally to Home Assistant
I use it for [Blurt](https://github.com/QuantiusBenignus/blurt#network-transcription)
gnome shell extension.

You need a running Whisper compatible API service, for example Whisper.cpp instance:

https://github.com/ggerganov/whisper.cpp/tree/master/examples/server

I run it on nvidia GPU with fantastic results with detailed inference on large model in usually about a second:

```sh
whisper.cpp/server -m whisper.cpp/models/ggml-large-v3-q5_0.bin --host 0.0.0.0 --port 8910 --print-realtime --print-progress
```

You need to study whisper.cpp to get more information about running its STT service.

## Local Install

Clone the repository and set up Python virtual environment:

```sh
git clone https://github.com/ser/wyoming-whisper-api-client
cd wyoming-whisper-api-client
script/setup
```

Run a server anyone can connect to:

```sh
./script/run --uri tcp://0.0.0.0:7891 --debug --api http://192.168.41.49:8910/inference
```

# Acknowledgements

1. It's a rewrite of Michael Hansen's wyoming-faster-whisper.
2. Tests are not functioning as there is no public Whisper API service to test it out.

# Support

Matrix: #wyoming-whisper-api-client:sergevictor.eu
