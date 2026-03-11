#!/bin/bash
echo "🚀 Agentic Airflow - Ubuntu 24.04 Compatible!"

# Create & activate virtualenv FIRST
python3 -m venv agentic_env
source agentic_env/bin/activate

# Install dependencies in virtualenv
pip install --upgrade pip
pip install pyautogen==0.4.0 openai colorama

# Run agent
python airflow1_agent.py

echo "🎉 Airflow ready on port 8081!"
