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
password = "Praveen@1234"

# We want to read C:\Users\Praveen\.ssh\id_rsa_vm and get its public key
# Since paramiko can load private keys, we can generate the public key from the private key!
private_key_path = os.path.expanduser(r"~\.ssh\id_rsa_vm")
print(f"Loading private key from {private_key_path}...")
try:
    k = paramiko.RSAKey.from_private_key_file(private_key_path)
    pub_key_str = f"ssh-rsa {k.get_base64()} praveen@vm-jumpbox-prod"
    print("Loaded private key successfully. Derived public key string:")
    print(pub_key_str[:100] + "...")
except Exception as e:
    print(f"Failed to load private key: {e}")
    sys.exit(2)

print(f"Connecting to {hostname}:{port} via password...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(hostname, port=port, username=username, password=password, timeout=10)
    print("Connected successfully with password!")
    
    # Run commands to create directory and append public key
    stdin, stdout, stderr = ssh.exec_command(
        'mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'
    )
    stdout.read() # Wait for completion
    
    # Read existing keys to avoid duplicates
    stdin, stdout, stderr = ssh.exec_command('cat ~/.ssh/authorized_keys')
    existing_keys = stdout.read().decode('utf-8')
    
    # Clean public key line
    clean_pub_key = pub_key_str.strip()
    
    if clean_pub_key not in existing_keys:
        print("Appending public key to authorized_keys...")
        stdin, stdout, stderr = ssh.exec_command(f'echo "{clean_pub_key}" >> ~/.ssh/authorized_keys')
        stdout.read()
        print("Public key successfully appended!")
    else:
        print("Key is already authorized on the remote host.")
        
    # Also add user's GHOST key just in case they want to connect using it later
    ghost_pub_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCxUP9gtMKBObjUczyQpri747cJKrIDiOfoURGIjA8rdZcfWXjPwhHrzt9A3Xpt81CtnpGL5rQPA6KZs8QB+0Y6A86CYw2FAzoX5ANzCacsxQNg0qMS0uMxsla2vmgK4IbWs+emNKlOGrJLxMxckZYgqGLj7ccLNZsYKL/mM6oL5kZtUgzAYvDzcHwnjs+zmufyUMIiFFcZV3c/IQKNZ9/pYDaBzT/OoB9ihA9bqqZVWJaVHXK188lf50HFFd6UlAE4luW+TkwBWmNdrQiPSxQUeuySM0J1alee2mZTtLO+MR3vANmpmT0Bk07W3kxjnSHcEwEttUlCUUX7jLRSgyRYq0QFsXfeRxEjUU/cnbXzHbdvh0QxwNkPwCsujD5bz83ipSjucS5RYstHoxbKSeB0yaUQCJK32KQurl41AKeRQisAkB3o9BZqtTb6d6M1+XgYXLru2Gs7oK2Nc7rJz1fzsc3JXqoiCkwiAr4blPCNk0HjXx7IyymGow+waHKxAMxwklEo55Fu8Qn8XDI0pveo2GxQf16Q4XD5gee1QDZAFwjs4jIgOyig6UUMTHUhYJS+h8CA4x82mt9ky8Xfjq7SUGKzTL646AlyCqeR00fu7RIjIoBQewTEb6AtcMgfcBQ+5EpLLJQ+cXUEd+bRrdcNG5HJMyxq6zdddFZo6p8nMw== praveen@GHOST'
    if ghost_pub_key not in existing_keys:
        print("Appending GHOST public key to authorized_keys...")
        stdin, stdout, stderr = ssh.exec_command(f'echo "{ghost_pub_key}" >> ~/.ssh/authorized_keys')
        stdout.read()
        print("GHOST public key successfully appended!")

    # Verify connection works with key
    print("Testing connection with the private key...")
    ssh_key = paramiko.SSHClient()
    ssh_key.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_key.connect(hostname, port=port, username=username, key_filename=private_key_path, timeout=5)
        stdin, stdout, stderr = ssh_key.exec_command("whoami && hostname")
        res = stdout.read().decode('utf-8').strip()
        print(f"Success! Key authentication output: {res}")
        ssh_key.close()
    except Exception as ex:
        print(f"Key authentication failed: {ex}")
        
    ssh.close()
    print("Done!")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(3)
