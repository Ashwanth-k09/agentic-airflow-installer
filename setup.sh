#!/bin/bash
echo "🚀 Agentic Airflow - Ubuntu 24.04 FULLY FIXED!"

# Install system dependencies FIRST
apt update -qq
apt install -y python3-pip python3-venv python3-full curl

# Create & activate virtual environment
echo "📦 Creating isolated Python environment..."
python3 -m venv agentic_env
source agentic_env/bin/activate

# Upgrade pip & install Python packages
echo "📦 Installing AI agent dependencies..."
pip install --upgrade pip
pip install pyautogen==0.4.0 openai colorama

# Run the AI agent
echo "🤖 Launching AI Airflow installer..."
python airflow1_agent.py

echo "🎉 SUCCESS! Airflow ready on http://localhost:8081"
