#!/bin/bash
# Serve the taxonomy editor on localhost:8090
# Then use pinggy to expose it:
#
# Terminal 1: Run this script
#   bash serve.sh
#
# Terminal 2: Run pinggy tunnel
#   while true; do 
#     ssh -p 443 -R0:localhost:8090 -L4302:localhost:4300 \
#       -o StrictHostKeyChecking=no -o ServerAliveInterval=30 \
#       9qPZIGXw1bk+force@ap.pro.pinggy.io
#     sleep 10
#   done

PORT=${1:-8090}
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Serving taxonomy editor at http://localhost:$PORT"
echo "Files in: $DIR"
echo ""
echo "To expose via pinggy, run in another terminal:"
echo "  ssh -p 443 -R0:localhost:$PORT -o StrictHostKeyChecking=no -o ServerAliveInterval=30 9qPZIGXw1bk+force@ap.pro.pinggy.io"
echo ""

cd "$DIR"
python3 -m http.server $PORT