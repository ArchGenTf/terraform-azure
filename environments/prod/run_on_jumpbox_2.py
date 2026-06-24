import sys
import os

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
    # 1. Install Helm using official shell script
    "curl -fsSL -o /tmp/get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && chmod +x /tmp/get_helm.sh && sudo /tmp/get_helm.sh",
    
    # 2. Get AKS credentials (admin)
    "az aks get-credentials --resource-group rg-archgen-prod --name aks-archgen-prod --admin --overwrite-existing",
    
    # 3. Test kubectl
    "kubectl get nodes",
    "kubectl get ns",
    "helm list -A"
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
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        
        if out:
            print("STDOUT:")
            print(out)
        if err:
            print("STDERR:")
            print(err)
            
    ssh.close()
    print("\nDone!")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(2)
