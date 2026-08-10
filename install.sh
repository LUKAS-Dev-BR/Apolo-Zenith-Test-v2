#!/bin/bash

set -e

echo "=== Apolo Zenith 1.9 - Instalação ==="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Erro: Node.js não encontrado. Por favor, instale Node.js 18+"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Erro: npm não encontrado. Por favor, instale npm"
    exit 1
fi

echo "=== Instalando dependências do backend ==="

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

echo "=== Instalando dependências do frontend ==="

# Navigate to frontend directory
cd frontend

# Install npm dependencies
npm install

cd ..

echo "=== Instalação concluída ==="
echo ""
echo "Para iniciar o backend:"
echo "  source venv/bin/activate"
echo "  cd backend"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Para iniciar o frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Ou use Docker Compose:"
echo "  docker-compose up"
