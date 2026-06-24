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
    # 1. Delete old nginx ingress applications from ArgoCD
    "kubectl delete application ingress-nginx-dev ingress-nginx-prod -n argocd --ignore-not-found",
    
    # 2. Hard refresh and sync all applications to pick up git changes
    "kubectl get applications.argoproj.io -n argocd -o jsonpath='{.items[*].metadata.name}'"
]

print(f"Connecting to {hostname}:{port} via key {private_key_path}...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(hostname, port=port, username=username, key_filename=private_key_path, timeout=10)
    print("Connected successfully!")
    
    # Step 1: Delete nginx apps
    print("\n--- Deleting old nginx controller applications ---")
    stdin, stdout, stderr = ssh.exec_command(commands[0])
    print(stdout.read().decode('utf-8'))
    print(stderr.read().decode('utf-8'))
    
    # Step 2: Get all app names
    stdin, stdout, stderr = ssh.exec_command(commands[1])
    app_names = stdout.read().decode('utf-8').strip().split()
    
    # Filter out deleted apps if they show up
    app_names = [app for app in app_names if app not in ['ingress-nginx-dev', 'ingress-nginx-prod']]
    
    print(f"Found applications to refresh: {app_names}")
    
    # Step 3: Hard refresh and patch each app
    for app in app_names:
        print(f"\n--- Hard refreshing app: {app} ---")
        # Add the refresh=hard annotation
        patch_refresh_cmd = 'kubectl patch application ' + app + ' -n argocd --type merge -p \'{"metadata": {"annotations": {"argocd.argoproj.io/refresh": "hard"}}}\''
        stdin, stdout, stderr = ssh.exec_command(patch_refresh_cmd)
        print(stdout.read().decode('utf-8').strip())
        
        # Initiate sync
        patch_sync_cmd = 'kubectl patch application ' + app + ' -n argocd --type merge -p \'{"operation": {"sync": {}}}\''
        stdin, stdout, stderr = ssh.exec_command(patch_sync_cmd)
        print(stdout.read().decode('utf-8').strip())
        
    ssh.close()
    print("\nDone!")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(2)
