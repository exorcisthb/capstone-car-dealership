#!/usr/bin/env bash
# ============================================================
# Start Django + ngrok for public URL
# Requires NGROK_AUTHTOKEN env var (free signup at ngrok.com)
# ============================================================
set -e

cd ~/xrwvm-fullstack_developer_capstone
source .venv/bin/activate

# Start Django in the background
echo "=== Starting Django on port 8000 ==="
cd server
nohup python manage.py runserver 0.0.0.0:8000 > ~/django.log 2>&1 &
DJANGO_PID=$!
echo "Django PID: $DJANGO_PID"
sleep 3

# Check Django is alive
if ! kill -0 $DJANGO_PID 2>/dev/null; then
    echo "ERROR: Django failed to start. Last log lines:"
    tail -20 ~/django.log
    exit 1
fi
echo "Django is running at http://localhost:8000"

# Start ngrok
cd ..
if [ -z "$NGROK_AUTHTOKEN" ]; then
    echo "WARNING: NGROK_AUTHTOKEN not set. ngrok will work but URL changes every restart."
    echo "Get a free authtoken at: https://dashboard.ngrok.com/get-started/your-authtoken"
fi

echo "=== Starting ngrok ==="
nohup ./ngrok http 8000 --log=stdout > ~/ngrok.log 2>&1 &
NGROK_PID=$!
echo "ngrok PID: $NGROK_PID"
sleep 5

# Get public URL from ngrok API
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for t in data.get('tunnels', []):
        if t.get('proto') == 'https':
            print(t['public_url'])
            break
except Exception as e:
    print('', file=sys.stderr)
")
if [ -z "$PUBLIC_URL" ]; then
    echo "ERROR: Could not get ngrok URL. Last ngrok log lines:"
    tail -20 ~/ngrok.log
    exit 1
fi

echo ""
echo "============================================================"
echo "DEPLOYED URL: $PUBLIC_URL"
echo "============================================================"
echo ""
echo "Save this URL in deploymentURL.txt:"
echo "  $PUBLIC_URL"
echo ""
echo "Press Ctrl+C to stop Django and ngrok."
echo ""

# Save URL to file for screenshot script
echo "$PUBLIC_URL" > ~/deployed_url.txt

# Wait for both
wait
