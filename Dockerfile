FROM debian:bookworm-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends git python3-pip bash \
 && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ser/wyoming-whisper-api-client
RUN pip3 install --no-cache-dir --break-system-packages -r wyoming-whisper-api-client/requirements.txt

WORKDIR /wyoming-whisper-api-client/
ADD run.sh ./
RUN chmod +x run.sh

ENTRYPOINT ["bash", "/wyoming-whisper-api-client/run.sh"]
