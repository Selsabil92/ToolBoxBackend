# services/zap_service.py
import os
import json
from datetime import datetime
from config.ssh_config import ssh_connect_and_execute

UPLOAD_FOLDER = 'uploads/scans'

def run_zap(target_ip):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    full_url = target_ip if target_ip.startswith("http") else f"http://{target_ip}"
    safe_target = full_url.replace("/", "_").replace(":", "_").replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"zap_result_{safe_target}_{timestamp}.json"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # ✅ Appel ZAP en mode daemon + spider + active scan
    command = f"""
        /usr/share/zaproxy/zap.sh -cmd -quickurl {full_url} -quickout /tmp/zap_output.json -quickprogress
        && cat /tmp/zap_output.json
    """

    try:
        output = ssh_connect_and_execute(
            command,
            '192.168.37.133',
            'root',
            '/root/.ssh/toolbox_key'
        )

        parsed = json.loads(output)

        result = {
            "status": "success",
            "target": full_url,
            "date": str(datetime.now()),
            "type": "zap-scan",
            "vulnerabilities": parsed.get("site", []),
            "scan_output": json.dumps(parsed, indent=2),
            "saved_as": filepath
        }

        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)

        return result

    except Exception as e:
        error = {
            "status": "error",
            "target": full_url,
            "date": str(datetime.now()),
            "type": "zap-scan",
            "error": str(e),
            "saved_as": filepath
        }
        with open(filepath, 'w') as f:
            json.dump(error, f, indent=2)

        return error
