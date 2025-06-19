import nmap
import os
import json
from datetime import datetime

UPLOAD_FOLDER = 'uploads/scans'  # ⚠ unification avec les autres rapports

def scan_vulnerabilities(target, scan_arguments="-sV --script vuln", verbose=False):
    scanner = nmap.PortScanner()

    vuln_data = {
        "target": target,
        "date": str(datetime.now()),
        "status": "success",
        "type": "vuln-analysis",  # ajouté pour uniformiser avec les autres scans
        "vulnerabilities": []
    }

    try:
        if verbose:
            print(f"[+] Scan des vulnérabilités sur {target} avec '{scan_arguments}'")

        scanner.scan(hosts=target, arguments=scan_arguments)

        # 🔍 DEBUG log complet
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        debug_path = os.path.join(UPLOAD_FOLDER, "last_scan_debug.txt")
        with open(debug_path, "w") as dbg:
            dbg.write(scanner.csv())

        for host in scanner.all_hosts():
            for proto in scanner[host].all_protocols():
                for port in scanner[host][proto].keys():
                    service = scanner[host][proto][port]
                    if verbose:
                        print(f"\n== {host}:{port}/{proto} ==")
                        print(json.dumps(service, indent=2))

                    # 🔍 Cherche dans 'script' si présent
                    scripts = service.get("script", {})
                    for script_name, output in scripts.items():
                        vuln_data["vulnerabilities"].append({
                            "host": host,
                            "port": port,
                            "protocol": proto,
                            "script": script_name,
                            "output": output
                        })

                    # 🔍 Ajout spécial pour les CVEs de vulners
                    if "cpe" in service and "vulners" in scripts:
                        cve_output = scripts["vulners"]
                        cves = [line for line in cve_output.split('\n') if "CVE-" in line or "EXPLOIT" in line]
                        for line in cves:
                            vuln_data["vulnerabilities"].append({
                                "host": host,
                                "port": port,
                                "protocol": proto,
                                "script": "vulners",
                                "output": line.strip()
                            })

    except Exception as e:
        vuln_data["status"] = "error"
        vuln_data["error_message"] = str(e)
        if verbose:
            print(f"[ERREUR] {e}")

    # 💾 Sauvegarde JSON finale (même format que les autres modules)
    safe_target = target.replace("/", "_").replace(".", "_")
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    filename = f"vuln-analysis_resultat_{safe_target}.json"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "w") as f:
        json.dump(vuln_data, f, indent=4)

    if verbose:
        print(f"[✓] Résultats enregistrés dans {filepath}")
        print(f"[✓] Vulnérabilités détectées : {len(vuln_data['vulnerabilities'])}")

    vuln_data["saved_as"] = filepath
    return vuln_data
