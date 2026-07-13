#!/bin/bash

# Service Manager Launcher
# Custom port to avoid conflicts

PORT=8050

echo "🚀 Starting Django Service Manager on port $PORT..."
echo ""
echo "📍 Access URLs:"
echo "   Dashboard: http://127.0.0.1:$PORT/"
echo "   Admin:     http://127.0.0.1:$PORT/admin/"
echo ""

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run server
python manage.py runserver $PORT
