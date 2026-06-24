import os
import subprocess
import sys

if len(sys.argv) < 3:
    print("Usage: patch_argocd.py <resource_group> <cluster_name>")
    sys.exit(1)

rg = sys.argv[1]
cluster = sys.argv[2]

# If running in CI/CD (GHA) with service principal credentials
client_id = os.environ.get("ARM_CLIENT_ID")
client_secret = os.environ.get("ARM_CLIENT_SECRET")
tenant_id = os.environ.get("ARM_TENANT_ID")

if client_id and client_secret and tenant_id:
    print("CI/CD Environment detected. Logging in to Azure CLI using Service Principal...")
    login_cmd = [
        "az", "login", "--service-principal",
        "-u", client_id,
        "-p", client_secret,
        "--tenant", tenant_id
    ]
    # Run login command but mask password in output
    print(f"Executing: az login --service-principal -u {client_id} -p **** --tenant {tenant_id}")
    login_res = subprocess.run(login_cmd, capture_output=True, text=True)
    if login_res.returncode != 0:
        print("Azure CLI login failed:")
        print(login_res.stdout)
        print(login_res.stderr)
        sys.exit(login_res.returncode)
    print("Logged in successfully.")

cmd = [
    "az", "aks", "command", "invoke",
    "--resource-group", rg,
    "--name", cluster,
    "--command", 'kubectl patch svc argocd-server -n argocd -p \'{"spec": {"type": "LoadBalancer"}}\''
]

print(f"Executing: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
sys.exit(result.returncode)
