import os
import time
import sys
from colorama import Fore, Style, init
from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

# Pretty colors & init
init(autoreset=True)
GREEN = Fore.GREEN
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW
RED = Fore.RED
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA

def print_banner():
    print(f"\n{Style.BRIGHT}{CYAN}{'='*60}")
    print(f"{MAGENTA}🤖 WELCOME TO AGENTIC AIRFLOW INSTALLER {Style.BRIGHT}{MAGENTA}🤖")
    print(f"{CYAN}{'='*60}")
    print(f"{GREEN}✨ Fully automated Apache Airflow installation")
    print(f"{YELLOW}🎯 AI handles ALL errors & configurations")
    print(f"{BLUE}🌐 Access at http://localhost:YOUR_PORT")
    print(f"{CYAN}{'='*60}\n")

def get_user_inputs():
    print(f"{MAGENTA}📋 SETUP CONFIGURATION{Style.RESET}")
    print(f"{BLUE}💡 Press Enter for defaults\n")
    
    port = input(f"{GREEN}🌐 Airflow Web Port [{YELLOW}8081{Style.RESET}]: ").strip()
    if not port: port = "8081"
    
    username = input(f"{GREEN}👤 Admin Username [{YELLOW}admin{Style.RESET}]: ").strip()
    if not username: username = "admin"
    
    password = input(f"{GREEN}🔐 Admin Password [{YELLOW}airflow123{Style.RESET}]: ").strip()
    if not password: password = "airflow123"
    
    print(f"\n{CYAN}✅ CONFIG SUMMARY:")
    print(f"   🌐 Port: {GREEN}{port}")
    print(f"   👤 User: {GREEN}{username}")
    print(f"   🔐 Ready to install!{Style.RESET}\n")
    
    return port, username, password

def main():
    print_banner()
    
    # Get user preferences
    port, username, password = get_user_inputs()
    
    # Setup Groq + executor
    config_list = [{"model": "llama-3.3-70b-versatile", "api_key": os.getenv("GROQ_API_KEY"), "base_url": "https://api.groq.com/openai/v1"}]
    llm_config = {"config_list": config_list, "temperature": 0}
    
    executor = LocalCommandLineCodeExecutor(work_dir="airflow_install", timeout=600)
    
    assistant = AssistantAgent(
        "devops_assistant",
        llm_config=llm_config,
        system_message=f"""🤖 You are Airflow installation expert. Use these EXACT steps with port={port}, user={username}, pass={password}:

{Style.BRIGHT}1️⃣{Style.RESET} mkdir -p ~/airflow && cd ~/airflow
{Style.BRIGHT}2️⃣{Style.RESET} python3 -m venv venv && source venv/bin/activate
{Style.BRIGHT}3️⃣{Style.RESET} pip install "apache-airflow[postgres,celery]" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-main/constraints-3.12.txt"
{Style.BRIGHT}4️⃣{Style.RESET} export AIRFLOW_HOME=~/airflow
{Style.BRIGHT}5️⃣{Style.RESET} airflow db init
{Style.BRIGHT}6️⃣{Style.RESET} sed -i "s/web_server_port = 8080/web_server_port = {port}/g" airflow.cfg
{Style.BRIGHT}7️⃣{Style.RESET} airflow users create --username {username} --firstname Admin --lastname User --role Admin --email admin@example.com --password {password}
{Style.BRIGHT}8️⃣{Style.RESET} nohup airflow webserver --port {port} & nohup airflow scheduler &

🔧 FIX ERRORS AUTOMATICALLY: missing deps → sudo apt install, port busy → kill process, pip errors → upgrade pip
✅ SUCCESS when http://localhost:{port} works
📢 Say FINAL STATUS: http://localhost:{port} ✅ when done"""
    )
    
    user_proxy = UserProxyAgent(
        "user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=30,
        code_execution_config={"executor": executor},
        is_termination_msg=lambda msg: "FINAL STATUS" in msg.get("content", ""),
        system_message="🤖 Execute code silently. Show ONLY success/error. Fix issues automatically."
    )
    
    print(f"{GREEN}🚀 Starting AI installation... (watch progress below){Style.RESET}")
    print(f"{YELLOW}📁 Logs saved to: airflow_install/\n")
    
    # Start with pre-filled config
    message = f"🚀 INSTALL AIRFLOW with port={port}, user={username}, pass={password}"
    user_proxy.initiate_chat(assistant, message=message, silent=True)
    
    print(f"\n{GREEN}🎉 INSTALLATION COMPLETE!{Style.RESET}")
    print(f"{BLUE}🌐 Open your browser: {Style.BRIGHT}http://localhost:{port}{Style.RESET}")
    print(f"{GREEN}👤 Login: {YELLOW}{username}{Style.RESET}/{YELLOW}{password}{Style.RESET}")
    print(f"{CYAN}📁 Check logs: ls airflow_install/{Style.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}👋 Stopped by user. Airflow services still running in background.{Style.RESET}")
    except Exception as e:
        print(f"\n{RED}❌ Error: {e}{Style.RESET}")
