#!/bin/bash

# Pull the latest code from GitHub
git pull origin main

# Build the new Docker image
docker build -t crypto-noti-bot .

# Stop the old version and start the new one
docker stop crypto-bot-instance || true
docker rm crypto-bot-instance || true

docker run -d \
  --name crypto-bot-instance \
  --restart unless-stopped \
  --env-file .env \
  crypto-noti-bot