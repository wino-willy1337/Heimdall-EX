# file: modules/misc_utils.py

import subprocess
import os

def run_whois(target: str, output_dir: str):
    """Runs a whois lookup on the target domain."""
    print(f"[*] Running whois on {target}...")
    output_file = os.path.join(output_dir, f"{target}_whois.txt")
    command = ["whois", target]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"[+] whois lookup completed. Results saved to {output_file}")
    except FileNotFoundError:
        print("[!] whois command not found.")
    except subprocess.CalledProcessError as e:
        print(f"[!] whois failed. Error: {e.stderr}")

def run_curl_headers(target: str, output_dir: str):
    """Uses curl to grab HTTP headers from the target."""
    print(f"[*] Grabbing HTTP headers from http://{target} with curl...")
    output_file = os.path.join(output_dir, f"{target}_curl_headers.txt")
    command = ["curl", "-I", f"http://{target}"]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"[+] curl completed. Headers saved to {output_file}")
    except FileNotFoundError:
        print("[!] curl command not found.")
    except subprocess.CalledProcessError as e:
        print(f"[!] curl failed. Error: {e.stderr}")