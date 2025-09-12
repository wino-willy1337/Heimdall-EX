import subprocess
import shutil
import sys

def check_and_install_tool(tool_name: str, package_name: str = None):
    print(f"Checking for {tool_name}")

    if shutil.which(tool_name) is None:
        print(f"{tool_name} not found. Installing...")
        if package_name is None:
            package_name = tool_name
        try:
            subprocess.run(["sudo", "apt-get", "install", package_name], check=True)
            print(f"{tool_name} installed successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {tool_name}. Please install it manually.")
