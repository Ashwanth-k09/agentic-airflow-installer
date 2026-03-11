#!/bin/bash
echo "🚀 Agentic Airflow - BULLETPROOF EDITION!"

# Install ALL system deps
apt update -qq && apt install -y python3-pip python3-venv python3-full python3-dev build-essential

# Remove broken venv & recreate
rm -rf agentic_env
python3 -m venv agentic_env --clear

# Ensure pip works in venv
source agentic_env/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python
pip install --upgrade pip
pip install pyautogen==0.4.0 openai

# Run FIXED agent
python airflow1_agent_simple.py

echo "🎉 Airflow ready! http://localhost:8081 (admin/airflow123)"
