#!/bin/bash

# Setup script for REST vs GraphQL demo

echo "=========================================="
echo "  REST vs GraphQL Demo - Setup"
echo "=========================================="
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "  ✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To start the servers:"
echo "  Terminal 1: python src/rest/server.py"
echo "  Terminal 2: python src/graphql/server.py"
echo ""
echo "Or use: ./start-servers.sh"
echo "=========================================="
