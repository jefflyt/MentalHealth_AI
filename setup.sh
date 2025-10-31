#!/bin/bash

# AI Mental Health Agent - Setup Script
# This script sets up the Python environment and installs all dependencies

echo "🔧 Setting up AI Mental Health Agent..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install PyTorch first (recommended for stability)
echo "🔥 Installing PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install all requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys:"
    echo "   - GROQ_API_KEY: Get from https://console.groq.com/"
    echo "   - HUGGINGFACE_API_TOKEN: Get from https://huggingface.co/settings/tokens (optional)"
else
    echo "✓ .env file already exists"
fi

# Create chroma_db directory if it doesn't exist
if [ ! -d "chroma_db" ]; then
    echo "📊 Creating vector database directory..."
    mkdir -p chroma_db
else
    echo "✓ Vector database directory exists"
fi

echo ""
echo "🎉 Setup complete! Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: python test_core.py (to test the system)"
echo "3. Run: python app.py (to start the AI Mental Health Agent)"
echo "4. For full functionality, consider using Python 3.9-3.12"
echo ""
echo "To activate the environment in the future, run:"
echo "source venv/bin/activate"