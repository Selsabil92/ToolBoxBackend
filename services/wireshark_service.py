import subprocess
import os
import datetime

UPLOAD_DIR = "uploads/scans"

def run(target_ip):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        safe_ip = target_ip.replace('.', '-')
        pcap_filename = f"{timestamp}_wireshark_{safe_ip}.pcapng"
        pcap_path = os.path.join(UPLOAD_DIR, pcap_filename)

        # Capture réseau pendant 10s
        capture_command = ["tshark", "-i", "any", "-a", "duration:10", "-w", pcap_path]
        subprocess.run(capture_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)

        # Lecture du résumé
        summary_command = ["tshark", "-r", pcap_path, "-q", "-z", "io,phs"]
        output_raw = subprocess.check_output(summary_command, stderr=subprocess.STDOUT).decode()

        # Extraction entre les lignes ===
        lines = output_raw.splitlines()
        filtered = []
        recording = False
        for line in lines:
            if "Protocol Hierarchy Statistics" in line:
                recording = True
            if recording:
                filtered.append(line)

        result_clean = "\n".join(filtered).strip()

        return {
            "target": target_ip,
            "tool": "wireshark",
            "status": "success",
            "file": pcap_filename,
            "output": result_clean if result_clean else "Aucune donnée capturée"
        }

    except subprocess.CalledProcessError as e:
        return {"error": f"Erreur Wireshark : {e.output.decode()}"}
    except Exception as e:
        return {"error": str(e)}
