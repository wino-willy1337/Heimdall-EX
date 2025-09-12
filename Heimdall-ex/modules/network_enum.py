# file: modules/network_enum.py

import subprocess
import os
import re
from util.spinner import Spinner

def _parse_nmap_ports(scan_output: str) -> str:
    """Helper function to parse nmap output for open TCP ports."""
    ports = []
    port_pattern = re.compile(r'(\d+)/tcp\s+open')
    for line in scan_output.splitlines():
        match = port_pattern.search(line)
        if match:
            ports.append(match.group(1))
    return ",".join(ports)

def nmap_scan(target: str, output_dir: str):
    """
    Performs a deep, two-stage Nmap scan for comprehensive enumeration.
    Stage 1: Fast scan to find all open TCP ports.
    Stage 2: Detailed script, version, and OS scan on discovered ports.
    """
    print(f"[*] Starting In-Depth Nmap Scan on {target}...")
    os.makedirs(output_dir, exist_ok=True)
    
    # --- Stage 1: Fast Port Discovery ---
    stage1_file = os.path.join(output_dir, f"{target}_nmap_fast_scan.txt")
    print("[*] Stage 1: Discovering all open TCP ports...")
    stage1_command = ["sudo", "nmap", "-p-", "--min-rate=1000", "-T4", target, "-oN", stage1_file]
    
    spinner = Spinner("Running fast port scan (this may take a while)...")
    spinner.start()
    try:
        subprocess.run(stage1_command, capture_output=True, text=True, check=True)
        spinner.stop()
        print(f"[+] Stage 1 complete. Full port scan results saved to {stage1_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] Nmap Stage 1 failed. Error: {getattr(e, 'stderr', e)}")
        return

    # --- Parse Open Ports ---
    with open(stage1_file, 'r') as f:
        open_ports = _parse_nmap_ports(f.read())
    
    if not open_ports:
        print("[!] No open TCP ports found. Skipping detailed scan.")
        return
        
    print(f"[*] Discovered open ports: {open_ports}")

    # --- Stage 2: Detailed Scan on Open Ports ---
    stage2_file = os.path.join(output_dir, f"{target}_nmap_deep_scan.txt")
    print("[*] Stage 2: Running detailed scans on discovered ports...")
    stage2_command = ["sudo", "nmap", "-sC", "-sV", "-O", "-p", open_ports, target, "-oN", stage2_file]

    spinner = Spinner("Running detailed service, script, and OS scans...")
    spinner.start()
    try:
        subprocess.run(stage2_command, capture_output=True, text=True, check=True)
        spinner.stop()
        print(f"[+] Stage 2 complete. In-depth results saved to {stage2_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] Nmap Stage 2 failed. Error: {getattr(e, 'stderr', e)}")

def run_masscan(target: str, output_dir: str):
    """Runs a fast masscan on all TCP ports."""
    print(f"[*] Running Masscan on {target}...")
    output_file = os.path.join(output_dir, f"{target}_masscan.txt")
    command = ["sudo", "masscan", target, "-p1-65535", "--rate=1000", "-oG", output_file]
    
    spinner = Spinner("Running Masscan (rate=1000)...")
    spinner.start()
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        spinner.stop()
        print(f"[+] Masscan completed. Results saved to {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] Masscan failed. It may need sudo privileges. Error: {getattr(e, 'stderr', e)}")