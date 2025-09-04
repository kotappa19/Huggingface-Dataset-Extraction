#!/bin/bash

# Setup script for Hugging Face Dataset Extraction Tool
# This script creates a virtual environment and installs dependencies

echo "🚀 Setting up Hugging Face Dataset Extraction Tool..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv dataset_extraction

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source dataset_extraction/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "To use the tool:"
echo "1. Activate the virtual environment: source dataset_extraction/bin/activate"
echo "2. Run the extraction: python src/extract_dataset.py"
echo "3. Or view dataset info: python src/extract_dataset.py --info-only"
echo "4. Test the tool: python src/test_extraction.py"
echo "5. Run example: python src/example_usage.py"
echo ""
echo "For more options, run: python src/extract_dataset.py --help"
