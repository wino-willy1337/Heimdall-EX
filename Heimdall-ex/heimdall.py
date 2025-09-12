import os
import sys
import time

from util import dependencies, required_tools
from modules import network_enum

def banner():
    print("""
 _   _      _               _       _ _       _______  __
| | | | ___(_)_ __ ___   __| | __ _| | |     | ____\ \/ /
| |_| |/ _ \ | '_ ` _ \ / _` |/ _` | | |_____|  _|  \  / 
|  _  |  __/ | | | | | | (_| | (_| | | |_____| |___ /  \ 
|_| |_|\___|_|_| |_| |_|\__,_|\__,_|_|_|     |_____/_/\_\
         
          """)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(1)

def tool_check():
    print("Checking and installing required tools...")
    for tool, package in required_tools.required_tools:
        dependencies.check_and_install_tool(tool, package)
    print("All required tools are installed.")

def working_directory_setup():
    banner()
    input_dir = input("Enter the working directory (default: ./recon): ") or "./recon"
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    else:
        print(f"Directory {input_dir} already exists. Using existing directory.")
    return input_dir

def target_input():
    target = input("Enter the target IP address or domain: ")
    if not target or target.lower() in ["localhost", "127.0.0.1"]:
        print("Invalid target provided. Exiting.")
        sys.exit(1)
    if target.lower() == "exit":
        print("Exiting.")
        sys.exit(0)
    return target

def nmap(target, working_directory):
    network_enum.nmap_scan(target, working_directory)

def target_finder(subnet, working_directory):
    network_enum.run_target_finder(subnet, working_directory)

def setup():
    print("Setting up Heimdall-ex...")
    working_directory = working_directory_setup()
    target = target_input()
    print("Setup complete.")
    time.sleep(1)
    return target, working_directory

def main():
    print("Heimdall-ex - Automated Reconnaissance Tool")
    print("Version 1.0")
    tool_check()
    clear_screen()
    banner()
    print("Automated Reconnaissance Tool")
    print("Version 1.0")
    print("Author: wino_willy")
    subnet = input("Enter subnet target (e.g., 192.168.1.0/24): ")
    working_directory = working_directory_setup()
    target_finder(subnet, working_directory)
    target = target_input()
    print(f"Starting reconnaissance on {target}...")
    nmap(target, working_directory)
    print("Reconnaissance completed.")
    time.sleep(1)

if __name__ == "__main__":
    main()
    