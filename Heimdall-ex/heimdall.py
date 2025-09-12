import os
import subprocess
import sys
import time 


from util import dependencies, required_tools
from modules import network_enum, web_enum, dns_enum, smb_enum, snmp_enum, general_utils


print("Heimdall-ex - Automated Reconnaissance Tool")
print("Version 1.0")

#check and install required tools

def tool_check():
    print("Checking and installing required tools...")
    for tool, package in required_tools.required_tools:
        dependencies.check_and_install_tool(tool, package)

    print("All required tools are installed.")

def target_input():
    target = input("Enter the target IP address or domain: ")
    if not target:
        print("No target provided. Exiting.")
        sys.exit(1)
    elif target == "localhost":
        print("Localhost is not a valid target. Exiting.")
        sys.exit(1)
    elif target == "127.0.0.1":
        print("Loopback address is not a valid target. Exiting.")
        sys.exit(1)
    elif target.lower() == "exit":
        print("Exiting.")
        sys.exit(0)
    return target

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(1)

def banner():
    print("""
 _   _      _               _       _ _       _______  __
| | | | ___(_)_ __ ___   __| | __ _| | |     | ____\ \/ /
| |_| |/ _ \ | '_ ` _ \ / _` |/ _` | | |_____|  _|  \  / 
|  _  |  __/ | | | | | | (_| | (_| | | |_____| |___ /  \ 
|_| |_|\___|_|_| |_| |_|\__,_|\__,_|_|_|     |_____/_/\_\
         
          """)

def working_directory_setup():
    banner()
    input_dir = input("Enter the working directory (default: ./recon): ") or "./recon"
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    else:
        print(f"Directory {input_dir} already exists. Using existing directory.")
    return input_dir

def nmap(target, working_directory):
    network_enum.nmap_scan(target, working_directory)

def main():
    tool_check()
    clear_screen()
    banner()
    print("Automated Reconnaissance Tool")
    print("Version 1.0")
    print("Author: wino_willy")
    working_directory = working_directory_setup()
    target = target_input()
    print(f"Starting reconnaissance on {target}...")
    nmap(target, working_directory)
    print("Reconnaissance completed.")

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    time.sleep(1)

if __name__ == "__main__":
    main()
    