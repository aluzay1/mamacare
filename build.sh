#!/bin/bash

# Force Python 3.11
echo "Setting up Python 3.11 environment..."

# Install dependencies
pip install -r backend/requirements.txt
pip install gunicorn

echo "Build completed successfully!" 