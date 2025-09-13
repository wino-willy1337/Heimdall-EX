# file: util/dependencies.py

import shutil
import subprocess
import sys

def check_and_install_tool(tool_name: str, package_name: str = None):
    """
    Checks if a tool is in the system's PATH, and if not, prompts to install it.
    This is a safer, more professional implementation.
    """
    if not package_name:
        package_name = tool_name

    print(f"[*] Verifying '{tool_name}'...")
    if shutil.which(tool_name):
        # The tool is already installed, no need to print anything extra.
        return True

    print(f"[!] '{tool_name}' is not found in PATH.")
    
    # Determine the package manager
    install_command = ""
    pm_found = ""
    if shutil.which("apt-get"):
        pm_found = "apt-get"
        install_command = f"sudo apt-get install -y {package_name}"
    elif shutil.which("pacman"):
        pm_found = "pacman"
        install_command = f"sudo pacman -S --noconfirm {package_name}"
    elif shutil.which("dnf"):
        pm_found = "dnf"
        install_command = f"sudo dnf install -y {package_name}"
    else:
        print(f"[!] Could not determine a supported package manager. Please install '{package_name}' manually.")
        return False

    # Prompt the user for permission to install
    try:
        user_input = input(f"    Attempt to install it using '{pm_found}'? [y/N]: ")
    except KeyboardInterrupt:
        print("\n[!] User cancelled. Aborting dependency installation.")
        return False
        
    if user_input.lower() == 'y':
        print(f"[*] Running installation command. You may be prompted for your password.")
        try:
            # We don't use shell=True for security. We pass the command as a list.
            subprocess.run(install_command.split(), check=True)
            if shutil.which(tool_name):
                print(f"[+] '{tool_name}' installed successfully.")
                return True
            else:
                print(f"[!] Installation command ran, but '{tool_name}' is still not in PATH.")
                return False
        except subprocess.CalledProcessError as e:
            print(f"[!] Installation command failed with error: {e}")
            return False
    else:
        print("[!] Installation declined by user.")
        return False