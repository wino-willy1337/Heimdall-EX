# file: modules/snmp_enum.py

import subprocess
import os

def run_snmpcheck(target: str, output_dir: str):
    """Runs snmpcheck against the target."""
    print(f"[*] Running snmpcheck on {target}...")
    output_file = os.path.join(output_dir, f"{target}_snmpcheck.txt")
    command = ["snmpcheck", "-t", target]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"[+] snmpcheck scan completed. Results saved to {output_file}")
    except FileNotFoundError:
        print("[!] snmpcheck command not found.")
    except subprocess.CalledProcessError as e:
        print(f"[!] snmpcheck failed. Error: {e.stderr}")