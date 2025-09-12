# file: heimdall.py

import os
import sys
import time
from util import dependencies, required_tools
from modules import network_enum, web_enum, dns_enum, smb_enum, snmp_enum, misc_utils

def banner():
    print("""
 _   _      _               _       _ _       _______  __
| | | | ___(_)_ __ ___   __| | __ _| | |     | ____\ \/ /
| |_| |/ _ \ | '_ ` _ \ / _` |/ _` | | |_____|  _|  \  / 
|  _  |  __/ | | | | | | (_| | (_| | | |_____| |___ /  \ 
|_| |_|\___|_|_| |_| |_|\__,_|\__,_|_|_|     |_____/_/\_\
         
    """)
    print("Author: wino_willy | Version 1.2")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def tool_check():
    """Checks for all required tools before the main program runs."""
    print("[*] Checking for required tools...")
    tools_to_check = required_tools.required_tools
    for tool, package in tools_to_check:
        dependencies.check_and_install_tool(tool, package)
    print("[+] All required tools are installed and ready.")
    time.sleep(2)

def get_working_directory():
    """Prompts the user to set a working directory."""
    input_dir = input("Enter the working directory (default: ./recon): ") or "./recon"
    os.makedirs(input_dir, exist_ok=True)
    print(f"[*] Working directory set to: {input_dir}")
    return input_dir

def get_target():
    """Prompts the user for a target IP or domain."""
    target = input("Enter the target IP address or domain: ")
    if not target:
        print("[!] Invalid target provided. Exiting.")
        sys.exit(1)
    return target

# --- Sub-Menu Functions ---

def web_menu(target, working_directory):
    while True:
        clear_screen(); banner()
        print(f"--- Web Enumeration Menu (Target: {target}) ---")
        print("1) Run Gobuster (dir scan)")
        print("2) Run Nikto (vulnerability scan)")
        print("3) Run WhatWeb (technology stack)")
        print("4) Run Dirb (dir scan)")
        print("5) Run ALL Web Scans")
        print("9) Back to Main Menu")
        choice = input("\nEnter choice: ")

        if choice == '1': web_enum.run_gobuster(target, working_directory)
        elif choice == '2': web_enum.run_nikto(target, working_directory)
        elif choice == '3': web_enum.run_whatweb(target, working_directory)
        elif choice == '4': web_enum.run_dirb(target, working_directory)
        elif choice == '5':
            web_enum.run_gobuster(target, working_directory)
            web_enum.run_nikto(target, working_directory)
            web_enum.run_whatweb(target, working_directory)
            web_enum.run_dirb(target, working_directory)
        elif choice == '9': return
        else: print("[!] Invalid choice.")
        input("\nPress Enter to continue...")

def network_menu(target, working_directory):
    while True:
        clear_screen(); banner()
        print(f"--- Network Scanning Menu (Target: {target}) ---")
        print("1) Run Nmap (Standard Scripts, Service Versions)")
        print("2) Run Masscan (Fast, All TCP Ports)")
        print("9) Back to Main Menu")
        choice = input("\nEnter choice: ")

        if choice == '1': network_enum.nmap_scan(target, working_directory)
        elif choice == '2': network_enum.run_masscan(target, working_directory)
        elif choice == '9': return
        else: print("[!] Invalid choice.")
        input("\nPress Enter to continue...")


# --- Main Menu ---

def main_menu(target, working_directory):
    """Displays the main tool menu to the user."""
    while True:
        clear_screen(); banner()
        print(f"Target: {target} | Outputting to: {working_directory}\n")
        print("Select a tool category to run:")
        print("  1) Network Scans")
        print("  2) Web Enumeration")
        print("  3) DNS Enumeration")
        print("  4) SMB Enumeration")
        print("  5) SNMP Enumeration")
        print("  6) Misc Utilities")
        print("  99) Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1': network_menu(target, working_directory)
        elif choice == '2': web_menu(target, working_directory)
        elif choice == '3': dns_enum.run_dnsrecon(target, working_directory)
        elif choice == '4': smb_enum.run_enum4linux(target, working_directory)
        elif choice == '5': snmp_enum.run_snmpcheck(target, working_directory)
        elif choice == '6': misc_utils.run_whois(target, working_directory)
        elif choice == '99':
            print("[*] Exiting Heimdall-EX. Goodbye!")
            sys.exit(0)
        else:
            print("[!] Invalid choice, please try again.")
            time.sleep(1)

def main():
    """Main function to run the framework."""
    clear_screen()
    banner()
    tool_check()
    
    working_directory = get_working_directory()
    target = get_target()
    
    main_menu(target, working_directory)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] User interrupted. Exiting.")
        sys.exit(0)
        