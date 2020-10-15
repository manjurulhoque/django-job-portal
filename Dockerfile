FROM python:3.8-slim-buster
LABEL maintainer="GeeksCAT<info@geekscat.org>"

WORKDIR /anem-per-feina/

RUN apt-get update \
    && apt-get install --no-install-recommends -qy wait-for-it \
    && rm -rf /var/lib/apt/list/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
