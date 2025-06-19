import paramiko
import os

KALI_IP = os.getenv("KALI_IP")
KALI_USER = os.getenv("KALI_USER")
KALI_PASSWORD = os.getenv("KALI_PASSWORD")

def run_nmap_scan(target):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(KALI_IP, username=KALI_USER, password=KALI_PASSWORD)
        command = f"nmap -sV {target}"
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        ssh.close()
        return {"status": "success", "output": output}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def analyze_results(scan_output):
    """
    Analyse la sortie d'un scan Nmap et renvoie les résultats sous forme structurée.
    Cette fonction peut être étendue selon le format de la sortie du scan (ici Nmap).
    """
    result = {
        "open_ports": [],
        "version_info": [],
    }

    lines = scan_output.splitlines()

    for line in lines:
        if "open" in line:
            result["open_ports"].append(line)
        if "version" in line:
            result["version_info"].append(line)

    return result
