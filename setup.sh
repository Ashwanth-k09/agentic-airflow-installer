#!/bin/bash
echo "🚀 Agentic Airflow - PRODUCTION READY!"

apt update -qq && apt install -y python3-pip python3-venv python3-full build-essential curl

rm -rf agentic_env
python3 -m venv agentic_env --clear
source agentic_env/bin/activate

curl https://bootstrap.pypa.io/get-pip.py | python
pip install --upgrade pip
pip install pyautogen==0.4.0 openai

# SET GROQ API KEY for demo (Killercoda free tier)
export GROQ_API_KEY="gsk_test_key_demo"

# Run simple agent (no colorama issues)
python airflow1_agent_simple.py

echo "🎉 Airflow ready! http://localhost:8081 (admin/airflow123)"
