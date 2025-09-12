# file: modules/smb_enum.py

import subprocess
import os
from util.spinner import Spinner

def run_nmap_smb_scripts(target: str, output_dir: str):
    """Runs a suite of Nmap's SMB enumeration and vulnerability scripts."""
    print(f"[*] Running Nmap SMB scripts on {target}...")
    output_file = os.path.join(output_dir, f"{target}_nmap_smb_scripts.txt")
    command = ["nmap", "-p", "139,445", "--script=smb-enum-shares,smb-enum-users,smb-os-discovery,smb-vuln*", target, "-oN", output_file]

    spinner = Spinner("Running Nmap SMB scripts...")
    spinner.start()
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        spinner.stop()
        print(f"[+] Nmap SMB scripts completed. Results saved to {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] Nmap SMB scripts failed. Error: {getattr(e, 'stderr', e)}")

def run_enum4linux_ng(target: str, output_dir: str):
    """Runs a full enum4linux-ng scan on the target."""
    print(f"[*] Running enum4linux-ng on {target}...")
    output_file = os.path.join(output_dir, f"{target}_enum4linux-ng.txt")
    command = ["enum4linux-ng", "-A", "-oJ", output_file, target]
    
    spinner = Spinner("Running enum4linux-ng (full enumeration)...")
    spinner.start()
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        spinner.stop()
        print(f"[+] enum4linux-ng scan completed. Results saved to {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] enum4linux-ng failed. Error: {getattr(e, 'stderr', e)}")

def run_smb_all(target: str, output_dir: str):
    """Orchestrates a full suite of SMB enumeration."""
    print(f"--- Starting Full SMB Enumeration on {target} ---")
    run_nmap_smb_scripts(target, output_dir)
    run_enum4linux_ng(target, output_dir)
    print(f"--- Full SMB Enumeration on {target} Complete ---")