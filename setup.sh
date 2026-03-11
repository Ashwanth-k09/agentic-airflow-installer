#!/bin/bash
echo "🚀 Agentic Airflow - ONE CLICK SETUP!"

# Install dependencies
pip3 install pyautogen==0.4.0 openai colorama

# Run agent
python3 airflow1_agent.py

echo "🎉 Airflow ready on port 8081!"
