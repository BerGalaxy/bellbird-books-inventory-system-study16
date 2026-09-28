#!/bin/bash
# Deployment script for Bellbird Books Inventory System

echo "Deploying Bellbird Books Inventory System..."

# Step 1: Create virtual environment
python -m venv .venv

# Step 2: Activate (Windows)
# .venv\Scripts\Activate.ps1

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run the application
python run.py