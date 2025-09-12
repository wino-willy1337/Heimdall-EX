# file: modules/general_utils.py

import subprocess
import os
from util.spinner import Spinner

def run_whois(target: str, output_dir: str):
    """Runs a whois lookup on the target domain."""
    print(f"[*] Running whois on {target}...")
    output_file = os.path.join(output_dir, f"{target}_whois.txt")
    command = ["whois", target]
    
    spinner = Spinner("Performing whois lookup...")
    spinner.start()
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        spinner.stop()
        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"[+] whois lookup completed. Results saved to {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] whois failed. Ensure target is a valid domain. Error: {getattr(e, 'stderr', e)}")

def run_curl_headers(target: str, output_dir: str):
    """Uses curl to grab HTTP headers from the target."""
    print(f"[*] Grabbing HTTP headers from http://{target} with curl...")
    output_file = os.path.join(output_dir, f"{target}_curl_headers.txt")
    command = ["curl", "-I", "--connect-timeout", "10", f"http://{target}"]

    spinner = Spinner("Grabbing HTTP headers...")
    spinner.start()
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        spinner.stop()
        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"[+] curl completed. Headers saved to {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] curl failed. Is the web server running? Error: {getattr(e, 'stderr', e)}")