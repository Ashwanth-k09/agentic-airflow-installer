#!/usr/bin/env python3
import os
import sys

print("\n" + "="*60)
print("🤖 AGENTIC AIRFLOW INSTALLER")
print("="*60)
print("✨ Fully automated Apache Airflow installation")
print("🎯 AI handles ALL errors automatically")
print("="*60 + "\n")

# Get inputs with defaults
port = input("🌐 Airflow Port [8081]: ").strip() or "8081"
username = input("👤 Username [admin]: ").strip() or "admin" 
password = input("🔐 Password [airflow123]: ").strip() or "airflow123"

print(f"\n✅ CONFIG: Port={port}, User={username}")
print("🚀 Starting installation...\n")

from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

config_list = [{"model": "llama-3.3-70b-versatile", "api_key": os.getenv("GROQ_API_KEY"), "base_url": "https://api.groq.com/openai/v1"}]
llm_config = {"config_list": config_list, "temperature": 0}

executor = LocalCommandLineCodeExecutor(work_dir="airflow_install", timeout=600)

assistant = AssistantAgent(
    "devops_assistant",
    llm_config=llm_config,
    system_message=f"""Install Airflow with port={port}, user={username}, pass={password}:
1. mkdir -p ~/airflow && cd ~/airflow
2. python3 -m venv venv && source venv/bin/activate  
3. pip install "apache-airflow[postgres,celery]" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-main/constraints-3.12.txt"
4. export AIRFLOW_HOME=~/airflow
5. airflow db init
6. sed -i "s/web_server_port = 8080/web_server_port = {port}/g" airflow.cfg
7. airflow users create --username {username} --firstname Admin --lastname User --role Admin --email admin@example.com --password {password}
8. nohup airflow webserver --port {port} & nohup airflow scheduler &
Fix ALL errors. Say "DONE: http://localhost:{port}" when working."""
)

user_proxy = UserProxyAgent(
    "user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"executor": executor},
    max_consecutive_auto_reply=30,
    is_termination_msg=lambda x: "DONE" in x.get("content", "")
)

user_proxy.initiate_chat(assistant, message=f"Install Airflow: port={port}, user={username}, pass={password}")

print("\n🎉 SUCCESS!")
print(f"🌐 http://localhost:{port}")
print(f"👤 {username}:{password}")
print("📁 Logs: ls airflow_install/")
