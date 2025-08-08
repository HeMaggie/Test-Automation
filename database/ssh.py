import paramiko

def ssh_run_command(ip, username, password, command):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    # Load system SSH known hosts
    ssh.load_system_host_keys()
    # Add missing host keys
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the server
        ssh.connect(ip, username=username, password=password)
        
        # Run the command
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Fetch the output and errors
        output = stdout.read().decode()
        errors = stderr.read().decode()
        
        return output, errors
    finally:
        # Close the connection
        ssh.close()

