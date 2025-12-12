from flask import Flask, request
import os
import requests

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')  # store in k8s secret
REPO = os.environ.get('REPO')  # e.g., myuser/resilient-deployment-demo
WORKFLOW_FILE = os.environ.get('WORKFLOW_FILE', 'rollback.yml')
REF = os.environ.get('REF', 'main')

@app.route('/alert', methods=['POST'])
def alert():
    payload = request.json
    # If any alert has severity=critical -> trigger rollback
    alerts = payload.get('alerts', [])
    for a in alerts:
        labels = a.get('labels', {})
        if labels.get('severity') == 'critical':
            trigger_rollback()
            break
    return '', 204

def trigger_rollback():
    url = f"https://api.github.com/repos/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    body = {"ref": REF, "inputs": {"triggered_by": "alertmanager"}}
    r = requests.post(url, json=body, headers=headers)
    print("triggered rollback:", r.status_code, r.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
