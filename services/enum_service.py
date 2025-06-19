import nmap
import json
import os
import uuid
from datetime import datetime

# 📁 Dossier d’archivage des rapports
REPORTS_FOLDER = 'saved_reports'
os.makedirs(REPORTS_FOLDER, exist_ok=True)

def nmap_scan(target, scan_arguments=None):
    scanner = nmap.PortScanner()
    if not scan_arguments:
        scan_arguments = "-sV -O -sC -A --script=vuln"

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    filename_timestamp = now.strftime("%d-%m-%Y-%H-%M-%S")
    safe_target = target.replace("/", "_").replace(":", "_")

    report_id = str(uuid.uuid4())
    report_filename = f"{filename_timestamp}_resultat_{safe_target}.json"
    report_path = os.path.join(REPORTS_FOLDER, report_filename)

    scan_data = {
        "report_id": report_id,
        "title": f"Scan Nmap de {target}",
        "target": target,
        "created_at": timestamp,
        "type": "Vulnerability Scan",
        "status": "completed",
        "filename": report_filename,
        "filepath": report_path,
        "scan_arguments": scan_arguments,
        "summary": {
            "total_hosts": 0,
            "total_open_ports": 0
        },
        "hosts": [],
    }

    try:
        scanner.scan(hosts=target, arguments=scan_arguments)
        total_open_ports = 0

        for host in scanner.all_hosts():
            host_data = {
                "host": host,
                "state": scanner[host].state(),
                "hostnames": scanner[host].get('hostnames', []),
                "protocols": [],
                "osmatches": [],
                "addresses": scanner[host].get('addresses', {}),
                "uptime_seconds": scanner[host].get('uptime', {}).get('seconds')
            }

            for proto in scanner[host].all_protocols():
                ports_data = []
                for port in sorted(scanner[host][proto].keys()):
                    service = scanner[host][proto][port]
                    ports_data.append({
                        "port": port,
                        "service": service.get("name", ""),
                        "version": service.get("version", "inconnue"),
                        "state": service.get("state", ""),
                        "scripts": service.get("script", {})
                    })
                    if service.get("state") == "open":
                        total_open_ports += 1

                host_data["protocols"].append({
                    "protocol": proto,
                    "ports": ports_data
                })

            if 'osmatch' in scanner[host]:
                host_data["osmatches"] = [
                    {"name": osmatch.get("name", ""), "accuracy": osmatch.get("accuracy", "")}
                    for osmatch in scanner[host]["osmatch"]
                ]

            scan_data["hosts"].append(host_data)

        scan_data["summary"]["total_hosts"] = len(scanner.all_hosts())
        scan_data["summary"]["total_open_ports"] = total_open_ports

    except Exception as e:
        scan_data["status"] = "failed"
        scan_data["error_message"] = str(e)

    with open(report_path, "w") as f:
        json.dump(scan_data, f, indent=4)

    return scan_data
