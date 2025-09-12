import subprocess
import os

def nmap_scan(target: str, output_dir: str):
    print(f"Running Nmap scan on {target}...")
    output_file = os.path.join(output_dir, f"{target}_nmap.txt")
    subprocess.run(["nmap", "-sC", "-sV", "-oN", output_file, target])
    print(f"Nmap scan completed. Results saved to {output_file}")