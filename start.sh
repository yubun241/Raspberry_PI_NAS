#!/bin/bash

# Desktop
cd ~/Desktop

# python
source ~/env1/bin/activate

echo "FastAPIReload..."
pkill -f uvicorn
pkill -f cloudflared
pkill -f "python3 -m http.server"

sleep 2

# FastAPI 
echo "FastAPI ..."
uvicorn main:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1 &

sleep 5

# Cloudflare Tunnel ??
echo "Cloudflare Tunnel ????..."
cloudflared tunnel --url http://localhost:8000 > tunnel.log 2>&1 &

# URL??
echo "Tunnel URL Connecting..."
sleep 5
URL=$(grep -o 'https://.*trycloudflare.com' tunnel.log | head -n 1)
echo "URL: $URL"

# send_url
if [ ! -z "$URL" ]; then
    python3 ./send_url.py "$URL"
fi

echo "Done"
