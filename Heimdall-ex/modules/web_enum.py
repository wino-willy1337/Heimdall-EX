# file: modules/web_enum.py

import subprocess
import os

def run_gobuster(target: str, output_dir: str):
    """Runs a gobuster dir scan on the target."""
    print(f"[*] Running Gobuster on http://{target}...")
    output_file = os.path.join(output_dir, f"{target}_gobuster.txt")
    # Using a common wordlist path, this could be made configurable later
    command = [
        "gobuster", "dir", "-u", f"http://{target}", 
        "-w", "/usr/share/wordlists/dirb/common.txt", "-o", output_file
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"[+] Gobuster scan completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Gobuster failed. Error: {e.stderr}")

def run_nikto(target: str, output_dir: str):
    """Runs a nikto scan on the target."""
    print(f"[*] Running Nikto on http://{target}...")
    output_file = os.path.join(output_dir, f"{target}_nikto.txt")
    command = ["nikto", "-h", f"http://{target}", "-output", output_file]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"[+] Nikto scan completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Nikto failed. Error: {e.stderr}")

def run_whatweb(target: str, output_dir: str):
    """Runs an whatweb scan on the target."""
    print(f"[*] Running WhatWeb on http://{target}...")
    output_file = os.path.join(output_dir, f"{target}_whatweb.txt")
    
    try:
        # WhatWeb doesn't have a direct output flag, so we capture and write
        result = subprocess.run(
            ["whatweb", f"http://{target}"], 
            check=True, capture_output=True, text=True
        )
        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"[+] WhatWeb scan completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] WhatWeb failed. Error: {e.stderr}")

def run_dirb(target: str, output_dir: str):
    """Runs a dirb scan on the target."""
    print(f"[*] Running Dirb on http://{target}...")
    output_file = os.path.join(output_dir, f"{target}_dirb.txt")
    command = ["dirb", f"http://{target}", "-o", output_file]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"[+] Dirb scan completed. Results saved to {output_file}")
    except FileNotFoundError:
        print("[!] dirb command not found.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Dirb failed. Error: {e.stderr}")