# file: modules/smb_enum.py

import subprocess
import os

def run_enum4linux(target: str, output_dir: str):
    """Runs enum4linux on the target."""
    print(f"[*] Running enum4linux on {target}...")
    output_file = os.path.join(output_dir, f"{target}_enum4linux.txt")
    command = ["enum4linux", "-a", target]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"[+] enum4linux scan completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] enum4linux failed. Error: {e.stderr}")