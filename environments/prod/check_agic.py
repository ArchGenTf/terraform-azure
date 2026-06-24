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
    "kubectl logs -n kube-system ingress-appgw-deployment-795c98d6dd-pghmq --tail 100",
    "kubectl get ingress -A"
]

print(f"Connecting to {hostname}:{port} via key {private_key_path}...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(hostname, port=port, username=username, key_filename=private_key_path, timeout=10)
    print("Connected successfully!")
    
    for cmd in commands:
        print(f"\n--- Running: {cmd} ---")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))
        
    ssh.close()
    print("\nDone!")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(2)
