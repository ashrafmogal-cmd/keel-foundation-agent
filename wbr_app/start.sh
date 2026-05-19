#!/bin/bash
# WBR Report App - Quick Start Script

cd /Users/a0m1sr5/wbr_app

# Kill any existing instance on port 8001
lsof -ti:8001 | xargs kill -9 2>/dev/null

# Activate venv and start server
source .venv/bin/activate
echo "Starting WBR Report App..."
echo "Open: http://127.0.0.1:8001"
echo ""
echo "Press Ctrl+C to stop"
echo ""
python main.py
