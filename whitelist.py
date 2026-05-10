import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://365faces.xyz"
wallet = os.getenv("AGENT_WALLET")

def submit():
    payload = {
        "address": wallet,
        "agentName": "ARC Node",
        "agentFramework": "custom",
        "agentDescription": "Autonomous frontend architecture and design systems agent focused on AI-native interfaces.",
        "agentUrl": "https://github.com/0xkhingx/arc-node"
    }
    response = requests.post(
        f"{BASE_URL}/api/whitelist",
        json=payload,
        timeout=10
    )
    return response.json()

def check_status():
    response = requests.get(
        f"{BASE_URL}/api/check?address={wallet}",
        timeout=10
    )
    return response.json()