#!/usr/bin/env bash
# ============================================================
# Capstone Project - One-shot setup for IBM SkillsBuild Lab
# Run this ONCE in the lab terminal.
# ============================================================
set -e

echo "=== [0/6] Installing system dependencies ==="
sudo apt-get update -qq
sudo apt-get install -y -qq python3-venv python3-pip ngrok > /dev/null 2>&1

cd ~

echo "=== [1/6] Cloning repository ==="
if [ ! -d "xrwvm-fullstack_developer_capstone" ]; then
    git clone https://github.com/exorcisthb/xrwvm-fullstack_developer_capstone.git
fi
cd xrwvm-fullstack_developer_capstone

echo "=== [2/6] Pulling latest changes ==="
git pull origin main

echo "=== [3/6] Setting up Python virtualenv ==="
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r server/requirements.txt

echo "=== [4/6] Running migrations and seeding data ==="
cd server
python manage.py migrate --noinput
python manage.py seed_data
cd ..

echo "=== [5/6] Downloading ngrok ==="
if [ ! -f "ngrok" ]; then
    curl -sL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -o ngrok.tgz
    tar -xzf ngrok.tgz
    rm ngrok.tgz
    chmod +x ngrok
fi

echo "=== [6/6] Setup complete ==="
echo ""
echo "To run the app, use:"
echo "  bash start_ngrok.sh"
echo ""
