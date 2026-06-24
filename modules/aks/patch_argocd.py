import subprocess
import sys

if len(sys.argv) < 3:
    print("Usage: patch_argocd.py <resource_group> <cluster_name>")
    sys.exit(1)

rg = sys.argv[1]
cluster = sys.argv[2]

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
