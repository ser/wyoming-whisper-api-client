# Wyoming Whisper API client

[Wyoming protocol](https://github.com/rhasspy/wyoming) server
for the Whisper API speech to text system.

My motivation was to establish a one working STT system for whole
household, additionally to Home Assistant
I use it for [Blurt](https://github.com/QuantiusBenignus/blurt#network-transcription)
gnome shell extension.

You need a running Whisper compatible API service.

## Free Whisper compatible API servers

### Nvidia Parakeet

Do not let the name fool you, this model works very efficiently on a CPU and it's the
model I am currently running for my needs.

I am using a docker version from this repository, but it's up to you how do you like to make it running.

https://github.com/chand1012/parakeet-server

### Whisper.cpp

Another example is Whisper.cpp instance which requires a GPU for speedy inference.

https://github.com/ggerganov/whisper.cpp/tree/master/examples/server

I run it on nvidia GPU with fantastic results with detailed inference on large model in usually about a second:

```sh
whisper.cpp/server -m whisper.cpp/models/ggml-large-v3-q5_0.bin --host 0.0.0.0 --port 8910 --print-realtime --print-progress
```

You need to study whisper.cpp to get more information about running its STT service.

## Installation

### Local

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

### Docker

(**Optional**) The image is already published in GHCR. Build locally with:

```sh
git clone https://github.com/ser/wyoming-whisper-api-client
cd wyoming-whisper-api-client
docker build -t ghcr.io/ser/wyoming-whisper-api-client:latest .
```

Run the container:

```sh
docker run -p 7891:7891 -it --rm --name wyoming-whisper-api-client ghcr.io/ser/wyoming-whisper-api-client:latest \
    --debug \
    --uri tcp://0.0.0.0:7891 \
    --api http://192.168.41.49:8910/inference
```

Attach for logging:

```sh
docker logs -f wyoming-whisper-api-client
```

Stop the container:

```sh
docker stop wyoming-whisper-api-client
```

# Acknowledgements

1. It's a rewrite of Michael Hansen's wyoming-faster-whisper.
2. Tests are not functioning as there is no public Whisper API service to test it out.

# Support

Matrix: `#serdev:sergevictor.eu`

# Contribution

I do not accept any code or documentation contributions which have not been previously agreed upon. This means the order of steps is as follows:

1. Open an issue or discussion topic first.
2. Have a conversation about the matter at hand.
3. Reach a consensus about both form and content of the contribution.
4. Wait for a yay/nay signal from me.

Please do not submit any pull requests before I ask for them, as they will be closed. This outlined, proven practice will save time for all involved.

# Alternatives

1. https://github.com/roryeckel/wyoming_openai - A proxy which handles STT and TTS in one.
