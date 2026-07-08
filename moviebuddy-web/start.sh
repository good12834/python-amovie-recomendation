#!/bin/bash
echo "🎬 Starting MovieBuddy Web Application..."
echo ""

echo "[1/2] Starting Flask Backend Server..."
cd "$(dirname "$0")/backend"
python app.py &
BACKEND_PID=$!

echo "[2/2] Starting React Frontend Server..."
cd "$(dirname "$0")/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers are starting!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait