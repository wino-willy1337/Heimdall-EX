# file: modules/dns_enum.py

import subprocess
import os
from util.spinner import Spinner

def run_dnsrecon(target: str, output_dir: str):
    """Runs a thorough dnsrecon scan on the target domain."""
    print(f"[*] Running dnsrecon on {target}...")
    # Saving as XML allows for easier parsing later if needed
    output_file = os.path.join(output_dir, f"{target}_dnsrecon.xml")
    command = ["dnsrecon", "-d", target, "-t", "std,axfr,zonewalk", "--xml", output_file]
    
    spinner = Spinner("Running dnsrecon (standard, axfr, zonewalk)...")
    spinner.start()
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        spinner.stop()
        print(f"[+] dnsrecon scan completed. Results saved to {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] dnsrecon failed. Error: {getattr(e, 'stderr', e)}")

def run_dnsenum(target: str, output_dir: str):
    """Runs a dnsenum scan on the target domain."""
    print(f"[*] Running dnsenum on {target}...")
    output_file = os.path.join(output_dir, f"{target}_dnsenum.xml")
    # --noreverse to speed up scan, -f with a good wordlist
    wordlist = "/usr/share/dnsenum/dns.txt"

    if not os.path.exists(wordlist):
        print(f"[!] Wordlist not found: {wordlist}. Skipping dnsenum.")
        return

    command = ["dnsenum", "--noreverse", "-f", wordlist, "--output", output_file, target]

    spinner = Spinner("Running dnsenum with wordlist...")
    spinner.start()
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        spinner.stop()
        print(f"[+] dnsenum scan completed. Results saved to {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] dnsenum failed. Error: {getattr(e, 'stderr', e)}")

def run_dns_all(target: str, output_dir: str):
    """Orchestrates a full suite of DNS enumeration."""
    print(f"--- Starting Full DNS Enumeration on {target} ---")
    run_dnsrecon(target, output_dir)
    run_dnsenum(target, output_dir)
    print(f"--- Full DNS Enumeration on {target} Complete ---")