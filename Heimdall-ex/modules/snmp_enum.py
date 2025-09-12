# file: modules/snmp_enum.py

import subprocess
import os
from util.spinner import Spinner

def run_snmpcheck(target: str, output_dir: str):
    """Runs snmpcheck against the target with community string 'public'."""
    print(f"[*] Running snmpcheck on {target}...")
    output_file = os.path.join(output_dir, f"{target}_snmpcheck.txt")
    command = ["snmpcheck", "-t", target, "-c", "public"]
    
    spinner = Spinner("Running snmpcheck...")
    spinner.start()
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        spinner.stop()
        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"[+] snmpcheck scan completed. Results saved to {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        # snmpcheck often returns 1 even on success, so we check stderr
        if "No SNMP response" in getattr(e, 'stderr', ''):
             print(f"\n[!] snmpcheck failed. No SNMP service found or community string is not 'public'.")
        else:
             print(f"\n[!] snmpcheck failed. Error: {getattr(e, 'stderr', e)}")