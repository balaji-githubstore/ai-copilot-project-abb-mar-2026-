#!/bin/bash

# Installation script for the Selenium pytest framework
# Run this script to set up the complete development environment

echo "=== Selenium Pytest Framework Setup ==="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install production dependencies
echo "📚 Installing production dependencies..."
pip install -r requirements.txt

# Ask if user wants development dependencies
read -p "🤔 Install development dependencies? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🛠️  Installing development dependencies..."
    pip install -r requirements-dev.txt
fi

# Verify installation
echo "✅ Verifying installation..."
python -c "import selenium, pytest, yaml, webdriver_manager; print('All core packages imported successfully!')"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Usage:"
echo "  - Activate environment: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
echo "  - Run tests: pytest"
echo "  - Run tests with HTML report: pytest --html=reports/report.html"
echo "  - Run specific test markers: pytest -m smoke"
echo "  - Run tests in parallel: pytest -n auto"
echo ""