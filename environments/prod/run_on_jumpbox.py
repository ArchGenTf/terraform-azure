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

commands = [
    # Get AKS credentials using admin role
    "az aks get-credentials --resource-group rg-archgen-prod --name aks-archgen-prod --admin --overwrite-existing",
    
    # Test connection
    "kubectl get nodes",
    "kubectl get namespaces"
]

print(f"Connecting to {hostname}:{port} via key {private_key_path}...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(hostname, port=port, username=username, key_filename=private_key_path, timeout=10)
    print("Connected successfully!")
    
    for cmd in commands:
        print(f"\n--- Running command: {cmd} ---")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Read output line by line to show progress
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        
        if out:
            print("STDOUT:")
            print(out)
        if err:
            print("STDERR:")
            print(err)
            
    ssh.close()
    print("\nAll commands executed.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(2)
