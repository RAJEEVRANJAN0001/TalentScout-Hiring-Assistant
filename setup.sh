#!/bin/bash
# TalentScout Hiring Assistant - Automated Setup Script

echo "🚀 TalentScout Hiring Assistant - Setup Script"
echo "=============================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $python_version"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Setup .env file
echo "🔑 Setting up environment variables..."
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists. Keeping existing configuration."
else
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your Gemini API key!"
    echo "   Get your key from: https://makersuite.google.com/app/apikey"
fi
echo ""

echo "✨ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env file and add your GEMINI_API_KEY"
echo "   2. Run: source venv/bin/activate"
echo "   3. Run: streamlit run app.py"
echo ""
echo "🎉 Happy hiring!"
