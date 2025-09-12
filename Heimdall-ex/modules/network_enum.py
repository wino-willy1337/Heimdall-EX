import subprocess
import os
def run_target_finder(target: str, output_dir: str=None):
    print(f"Running targetfinder on {target}...")
    result = subprocess.run(
        ["nmap", "-F", "--max-retries", "3", target],
        capture_output=True,
        text=True
    )
    print("Targetfinder scan completed. Results:")
    print(result.stdout)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{target}_targetfinder.txt")
        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"Targetfinder results saved to {output_file}")


def nmap_scan(target: str, output_dir: str):
    print(f"Running Nmap scan on {target}...")
    output_file = os.path.join(output_dir, f"{target}_nmap.txt")
    subprocess.run(["nmap", "-sC", "-sV", "-oN", output_file, target])
    print(f"Nmap scan completed. Results saved to {output_file}")

def run_masscan(target: str, output_dir: str):
    """Runs a fast masscan on all TCP ports."""
    print(f"[*] Running Masscan on {target}...")
    output_file = os.path.join(output_dir, f"{target}_masscan.txt")
    # Note: Masscan can be very loud. Rate is set to 1000 packets/sec.
    command = ["masscan", target, "-p1-65535", "--rate=1000", "-oG", output_file]
    try:
        # Using sudo because masscan needs raw socket access
        subprocess.run(["sudo"] + command, check=True, capture_output=True, text=True)
        print(f"[+] Masscan completed. Results saved to {output_file}")
    except FileNotFoundError:
        print("[!] masscan command not found.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Masscan failed. It may need to be run with sudo. Error: {e.stderr}")