#!/bin/bash
# ZKDownloader Android Standalone Setup Script
# Termux me run karein: bash setup_android.sh

echo "🚀 ZKDownloader Android Setup Starting..."
echo ""

# Update packages
echo "📦 Updating packages..."
pkg update -y && pkg upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python..."
pkg install python -y

# Install git (if needed)
echo "📥 Installing git..."
pkg install git -y

# Install Python packages
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install yt-dlp flask

# Create app directory
echo "📁 Creating app directory..."
mkdir -p ~/ZKDownloader
cd ~/ZKDownloader

# Copy files (user ko manually karna hoga ya git se)
echo "📋 Files copy karein:"
echo "   - backend.py"
echo "   - index.html"
echo "   - app.js"
echo "   - style.css"
echo "   - manifest.json"
echo "   - requirements.txt"
echo "   - assets/ folder"
echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. App files ~/ZKDownloader/web_app/ me copy karein"
echo "2. Backend start karein: cd ~/ZKDownloader/web_app && python backend.py"
echo "3. Browser me jao: http://localhost:5000"
echo "4. PWA install karein (Add to Home Screen)"




