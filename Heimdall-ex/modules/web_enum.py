# file: modules/web_enum.py

import subprocess
import os
from util.spinner import Spinner

def run_gobuster(target: str, output_dir: str):
    """Runs a thorough gobuster dir scan on the target."""
    print(f"[*] Running Gobuster DIR scan on http://{target}...")
    output_file = os.path.join(output_dir, f"{target}_gobuster_dir.txt")
    extensions = "php,html,txt,js,aspx,asp"
    wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
    
    if not os.path.exists(wordlist):
        print(f"[!] Wordlist not found: {wordlist}. Skipping Gobuster DIR scan.")
        return

    command = ["gobuster", "dir", "-u", f"http://{target}", "-w", wordlist, "-x", extensions, "-t", "50", "-o", output_file]
    
    spinner = Spinner(f"Gobuster scanning directories...")
    spinner.start()
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        spinner.stop()
        print(f"[+] Gobuster DIR scan completed. Results saved to {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] Gobuster DIR scan failed. Error: {getattr(e, 'stderr', e)}")

def run_gobuster_vhost(target: str, output_dir: str):
    """Runs a gobuster vhost (subdomain) scan on the target."""
    print(f"[*] Running Gobuster VHOST scan on {target}...")
    output_file = os.path.join(output_dir, f"{target}_gobuster_vhost.txt")
    wordlist = "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt"

    if not os.path.exists(wordlist):
        print(f"[!] Wordlist not found: {wordlist}. Install with 'sudo apt install seclists'. Skipping VHOST scan.")
        return

    command = ["gobuster", "vhost", "-u", f"http://{target}", "-w", wordlist, "-t", "50", "-o", output_file]

    spinner = Spinner(f"Gobuster scanning for virtual hosts...")
    spinner.start()
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        spinner.stop()
        print(f"[+] Gobuster VHOST scan completed. Results saved to {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] Gobuster VHOST scan failed. Error: {getattr(e, 'stderr', e)}")

def run_nikto(target: str, output_dir: str):
    """Runs a nikto scan on the target."""
    print(f"[*] Running Nikto on http://{target}...")
    output_file = os.path.join(output_dir, f"{target}_nikto.txt")
    command = ["nikto", "-h", f"http://{target}", "-output", output_file, "-Tuning", "x 6"]
    
    spinner = Spinner("Running Nikto vulnerability scan...")
    spinner.start()
    try:
        # Nikto can return non-zero exit codes on normal scans, so we don't use check=True
        subprocess.run(command, capture_output=True, text=True)
        spinner.stop()
        print(f"[+] Nikto scan completed. Results saved to {output_file}")
    except FileNotFoundError as e:
        spinner.stop()
        print(f"\n[!] Nikto failed. Error: {e}")