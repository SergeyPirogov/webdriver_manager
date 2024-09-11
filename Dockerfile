FROM python:3.9-slim

ENV CHROME_VERSION=127.0.6533.72-1

RUN apt-get update && apt-get install -y wget && \
    wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb && \
    apt-get -y update && \
    apt-get install -y ./google-chrome-stable_${CHROME_VERSION}_amd64.deb;
