#!/usr/bin/env bash
set -e

echo "🚀 Starting ThaiTurk Development Servers..."
echo ""

# Check dependencies
command -v python >/dev/null 2>&1 || { echo "Python not found"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js not found"; exit 1; }

# Start backend
echo "📡 Starting Backend (port 8000)..."
cd 02_backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend
sleep 3

# Start frontend
echo "🌐 Starting Frontend (port 3000)..."
cd 01_frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Dev servers running:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Trap Ctrl+C to kill both
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM

# Wait for either to exit
wait
