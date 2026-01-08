#!/bin/bash

# Vietnamese Stock Analysis Web Server Startup Script

echo "=================================================="
echo "  Vietnamese Stock Analysis Web Server"
echo "=================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please create a virtual environment first:"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ../venv/bin/activate

# Check if required packages are installed
echo "📦 Checking dependencies..."
python -c "import fastapi" 2>/dev/null || {
    echo "❌ FastAPI not found. Installing..."
    pip install fastapi uvicorn[standard]
}

# Check if OAI_CONFIG_LIST exists
if [ ! -f "../OAI_CONFIG_LIST" ]; then
    echo "❌ OAI_CONFIG_LIST not found!"
    echo "Please create OAI_CONFIG_LIST with your Azure OpenAI configuration"
    exit 1
fi

# Start the server
echo ""
echo "🚀 Starting server on port 6900..."
echo "📊 Access UI at: http://localhost:6900"
echo "📚 API docs at: http://localhost:6900/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================================="
echo ""

python main.py
