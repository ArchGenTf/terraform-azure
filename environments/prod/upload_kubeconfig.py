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
local_kubeconfig = "prod_kubeconfig"

print(f"Connecting to {hostname}:{port} via key {private_key_path}...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(hostname, port=port, username=username, key_filename=private_key_path, timeout=10)
    print("Connected successfully!")
    
    # Create .kube directory on VM
    stdin, stdout, stderr = ssh.exec_command('mkdir -p ~/.kube && chmod 700 ~/.kube')
    stdout.read()
    
    # Upload kubeconfig
    sftp = ssh.open_sftp()
    print("Uploading kubeconfig to ~/.kube/config...")
    sftp.put(local_kubeconfig, '/home/praveen/.kube/config')
    sftp.chmod('/home/praveen/.kube/config', 0o600)
    sftp.close()
    print("Kubeconfig uploaded successfully!")
    
    # Test kubectl
    print("Testing kubectl get nodes on jumpbox VM...")
    stdin, stdout, stderr = ssh.exec_command('kubectl get nodes')
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    
    if out:
        print("STDOUT:")
        print(out)
    if err:
        print("STDERR:")
        print(err)
        
    ssh.close()
    print("Done!")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(2)
