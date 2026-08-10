#!/bin/bash

set -e

echo "=== Apolo Zenith 1.9 - Iniciando ==="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Ambiente virtual não encontrado. Execute install.sh primeiro."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start backend in background
echo "Iniciando backend..."
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "Iniciando frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "=== Apolo Zenith 1.9 iniciado ==="
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Pressione Ctrl+C para parar"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
