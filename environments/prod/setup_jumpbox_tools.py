import sys
import os
import time

try:
    import paramiko
except ImportError:
    print("paramiko is not installed.")
    sys.exit(1)

hostname = "127.0.0.1"
port = 2223
username = "praveen"
private_key_path = os.path.expanduser(r"~\.ssh\id_rsa_vm")

setup_script = """#!/usr/bin/env bash
set -e

echo "=== Starting Tool Installation ==="

# 1. Update and install prerequisites
sudo apt-get update
sudo apt-get install -y curl apt-transport-https ca-certificates gnupg git jq

# 2. Install Azure CLI
if ! command -v az &> /dev/null; then
    echo "Installing Azure CLI..."
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
else
    echo "Azure CLI already installed."
fi

# 3. Install kubectl
if ! command -v kubectl &> /dev/null; then
    echo "Installing kubectl..."
    sudo mkdir -p -m 755 /etc/apt/keyrings
    # Using the newer pkgs.k8s.io repository
    curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
    sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
    sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list
    sudo apt-get update
    sudo apt-get install -y kubectl
else
    echo "kubectl already installed."
fi

# 4. Install Helm
if ! command -v helm &> /dev/null; then
    echo "Installing Helm..."
    curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
    sudo apt-get update
    sudo apt-get install -y helm
else
    echo "Helm already installed."
fi

echo "=== Tool Installation Completed ==="
"""

print(f"Connecting to {hostname}:{port} via key {private_key_path}...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(hostname, port=port, username=username, key_filename=private_key_path, timeout=10)
    print("Connected successfully!")
    
    # Write setup script file to VM
    sftp = ssh.open_sftp()
    print("Uploading setup_tools.sh...")
    with sftp.file('/tmp/setup_tools.sh', 'w') as f:
        f.write(setup_script)
    sftp.chmod('/tmp/setup_tools.sh', 0o755)
    sftp.close()
    
    # Run setup script
    print("Running setup_tools.sh on jumpbox VM (this might take 1-2 minutes)...")
    stdin, stdout, stderr = ssh.exec_command('/tmp/setup_tools.sh')
    
    # Read output in real-time
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line, end='')
        
    err = stderr.read().decode('utf-8')
    if err:
        print("\n=== Errors / Warnings ===")
        print(err)
        
    ssh.close()
    print("\nSetup finished.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(2)
