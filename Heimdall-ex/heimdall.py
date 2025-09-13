# file: heimdall.py

import os
import sys
import time
from util import dependencies, required_tools
from modules import network_enum, web_enum, dns_enum, smb_enum, snmp_enum, general_utils

# ... (banner, clear_screen, tool_check, get_working_directory, get_target functions are unchanged) ...
def banner():
    print("""
 _   _      _               _       _ _       _______  __
| | | | ___(_)_ __ ___   __| | __ _| | |     | ____\ \/ /
| |_| |/ _ \ | '_ ` _ \ / _` |/ _` | | |_____|  _|  \  / 
|  _  |  __/ | | | | | | (_| | (_| | | |_____| |___ /  \ 
|_| |_|\___|_|_| |_| |_|\__,_|\__,_|_|_|     |_____/_/\_\
         
    """)
    print("Author: wino_willy | Version 2.1 - Refined")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def tool_check():
    """Checks for all required tools before the main program runs."""
    print("[*] Verifying all required external tools...")
    # Make sure to update required_tools.py to use 'enum4linux-ng'
    tools_to_check = required_tools.required_tools
    for tool, package in tools_to_check:
        dependencies.check_and_install_tool(tool, package)
    print("[+] All tool dependencies are satisfied.")
    time.sleep(2)

def get_working_directory():
    """Prompts the user to set a working directory."""
    input_dir = input("Enter working directory (default: ./recon): ") or "./recon"
    os.makedirs(input_dir, exist_ok=True)
    print(f"[*] Working directory set to: {input_dir}")
    return input_dir

def get_target():
    """Prompts the user for a target IP or domain."""
    target = input("Enter target IP or domain: ")
    if not target:
        print("[!] Invalid target. Exiting.")
        sys.exit(1)
    return target

# --- REFINED Sub-Menu Functions ---

def network_menu(target, wd):
    menu_actions = {
        '1': lambda: network_enum.nmap_scan(target, wd),
        '2': lambda: network_enum.run_masscan(target, wd, full_scan=False), # Fast Scan
        '3': lambda: network_enum.run_masscan(target, wd, full_scan=True),  # Full Scan
    }
    while True:
        clear_screen(); banner()
        print(f"--- Network Enumeration (Target: {target}) ---")
        print("1) Run In-Depth Nmap Scan (All TCP Ports + Scripts)")
        print("2) Run Masscan (FAST - Top 1000 Ports)")
        print("3) Run Masscan (FULL - All 65535 Ports - VERY SLOW)")
        print("9) Back to Main Menu")
        choice = input("\nEnter choice: ")

        action = menu_actions.get(choice)
        if action:
            action()
            input("\nPress Enter to continue...")
        elif choice == '9':
            return
        else:
            print("[!] Invalid choice.")
            time.sleep(1)

def web_menu(target, wd):
    menu_actions = {
        '1': lambda: web_enum.run_gobuster(target, wd),
        '2': lambda: web_enum.run_gobuster_vhost(target, wd),
        '3': lambda: web_enum.run_nikto(target, wd),
        '4': lambda: (web_enum.run_gobuster(target, wd), web_enum.run_gobuster_vhost(target, wd), web_enum.run_nikto(target, wd)),
    }
    while True:
        clear_screen(); banner()
        print(f"--- Web Enumeration (Target: {target}) ---")
        print("1) Run Gobuster (Directory Scan)")
        print("2) Run Gobuster (VHOST / Subdomain Scan)")
        print("3) Run Nikto (Vulnerability Scan)")
        print("4) Run ALL Web Scans")
        print("9) Back to Main Menu")
        choice = input("\nEnter choice: ")

        action = menu_actions.get(choice)
        if action:
            action()
            input("\nPress Enter to continue...")
        elif choice == '9':
            return
        else:
            print("[!] Invalid choice.")
            time.sleep(1)

# ... (The rest of main_menu, main, and __name__ == "__main__" are unchanged) ...
def dns_menu(target, wd):
    while True:
        clear_screen(); banner()
        print(f"--- DNS Enumeration (Target: {target}) ---")
        print("1) Run Dnsrecon (Zone Transfer & Standard Enum)")
        print("2) Run Dnsenum (Wordlist Bruteforce)")
        print("3) Run All DNS Scans")
        print("9) Back to Main Menu")
        choice = input("\nEnter choice: ")
        if choice == '1': dns_enum.run_dnsrecon(target, wd)
        elif choice == '2': dns_enum.run_dnsenum(target, wd)
        elif choice == '3': dns_enum.run_dns_all(target, wd)
        elif choice == '9': return
        else: print("[!] Invalid choice.")
        input("\nPress Enter to continue...")

# --- Main Logic ---

def main_menu(target, working_directory):
    """Displays the main tool menu and handles user choices."""
    menu_actions = {
        '1': network_menu,
        '2': web_menu,
        '3': dns_menu,
        '4': smb_enum.run_smb_all,
        '5': snmp_enum.run_snmpcheck,
        '6': general_utils.run_whois,
    }
    while True:
        clear_screen(); banner()
        print(f"Target: {target} | Saving results to: {working_directory}\n")
        print("  1) Network Scans")
        print("  2) Web Enumeration")
        print("  3) DNS Enumeration")
        print("  4) SMB Enumeration (Full Suite)")
        print("  5) SNMP Enumeration (Check 'public')")
        print("  6) General Utilities (Whois)")
        print(" 99) Exit")
        
        choice = input("\nEnter category: ")
        
        action = menu_actions.get(choice)
        if action:
            action(target, working_directory)
            input("\nPress Enter to return to the main menu...")
        elif choice == '99':
            print("[*] Exiting Heimdall-EX. Recon complete.")
            sys.exit(0)
        else:
            print("[!] Invalid choice.")
            time.sleep(1)

def main():
    """Main function to initialize and run the framework."""
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
        print("\n\n[*] User interruption detected. Exiting gracefully.")
        sys.exit(0)