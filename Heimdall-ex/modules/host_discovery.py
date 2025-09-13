# file: modules/host_discovery.py

import subprocess
import re
import netifaces
from util.spinner import Spinner

def get_local_network():
    """Gets the local network address in CIDR notation."""
    try:
        gateways = netifaces.gateways()
        default_gateway = gateways['default'][netifaces.AF_INET]
        interface = default_gateway[1]
        addrs = netifaces.ifaddresses(interface)
        netmask = addrs[netifaces.AF_INET][0]['netmask']
        # A more reliable way to calculate the CIDR prefix length
        prefix_len = sum(bin(int(x)).count('1') for x in netmask.split('.'))
        cidr = addrs[netifaces.AF_INET][0]['addr'] + '/' + str(prefix_len)
        return cidr
    except Exception as e:
        print(f"[!] Could not automatically determine local network: {e}")
        return None

def discover_hosts(network_range: str):
    """Discovers live hosts on the given network range using nmap."""
    print(f"[*] Discovering hosts on {network_range}...")
    command = ["sudo", "nmap", "-sn", network_range]
    
    spinner = Spinner("Scanning for live hosts...")
    spinner.start()
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        spinner.stop()
        
        # Parse the output to find live hosts
        hosts = []
        host_pattern = re.compile(r"Nmap scan report for (\S+)")
        for line in result.stdout.splitlines():
            match = host_pattern.search(line)
            if match:
                # Also capture the IP in parentheses if present
                ip_pattern = re.search(r"\((.*?)\)", line)
                if ip_pattern:
                    hosts.append(f"{match.group(1)} ({ip_pattern.group(1)})")
                else:
                    hosts.append(match.group(1))
        
        return hosts

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        spinner.stop()
        print(f"\n[!] Host discovery failed. Nmap needs to be run with sudo. Error: {getattr(e, 'stderr', e)}")
        return []