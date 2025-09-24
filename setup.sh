#!/bin/bash

echo "--- Starting Project Setup ---"

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install Python 3."
    exit
fi

# Create a virtual environment
echo "Creating Python virtual environment 'ai_doc_venv'..."
python3 -m venv ai_doc_venv

# Activate the virtual environment
source ai_doc_venv/bin/activate

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "--- Setup Complete! ---"
echo "Activate your environment to get started: source ai_doc_venv/bin/activate"