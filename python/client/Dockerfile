# Base image (not sure if actual) https://github.com/docker-library/python/blob/master/3.7/alpine3.11/Dockerfile
FROM python:3

LABEL authors="Arshan Hashemi, David Maulick"

WORKDIR /app

COPY client/requirements.txt /app
RUN cd /app && \
    pip install --no-cache-dir -r requirements.txt

# Included for network debugging
RUN apt-get update && \
    apt-get install -y net-tools dnsutils

COPY client /app
COPY util /app

CMD [ "python", "client.py", \ 
      "--cadence", "5" ]
