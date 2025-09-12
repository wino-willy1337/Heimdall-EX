# file: modules/dns_enum.py

import subprocess
import os

def run_dnsrecon(target: str, output_dir: str):
    """Runs a dnsrecon scan on the target domain."""
    print(f"[*] Running dnsrecon on {target}...")
    output_file = os.path.join(output_dir, f"{target}_dnsrecon.txt")
    command = ["dnsrecon", "-d", target, "-t", "std", "--xml", output_file]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"[+] dnsrecon scan completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] dnsrecon failed. Error: {e.stderr}")