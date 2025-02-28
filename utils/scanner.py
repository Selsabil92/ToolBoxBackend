# Scripts pour exécuter les outils de scan 
import subprocess # exécuter les scans via des appels système 

def run_nmap_scan(target):
    try:
        result = subprocess.run(["nmap", "-sV", target], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)
