import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://simcluster.ai"
TOKEN = os.getenv("SIMCLUSTER_TOKEN")

SKILL_HASH = "bfebfb90f585aca22e9672d283a46d5b0d1619aedf07e89ddab802ff0bdd5d8c"
SKILL_ACK = "alarm-shallow-window-crucial-push"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "X-Simcluster-Skill-Hash": SKILL_HASH,
    "X-Simcluster-Skill-Ack": SKILL_ACK
}

def mcp_call(method_name, arguments={}, call_id=1):
    response = requests.post(
        f"{BASE_URL}/mcp",
        headers=HEADERS,
        json={
            "jsonrpc": "2.0",
            "id": call_id,
            "method": "tools/call",
            "params": {
                "name": method_name,
                "arguments": arguments
            }
        },
        timeout=15
    )
    raw = response.text
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            data = line[5:].strip()
            if data:
                try:
                    return json.loads(data)
                except:
                    continue
    try:
        return response.json()
    except:
        return {"error": "Could not parse response", "raw": raw}

def list_tools():
    response = requests.post(
        f"{BASE_URL}/mcp",
        headers=HEADERS,
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        },
        timeout=15
    )
    raw = response.text
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            data = line[5:].strip()
            if data:
                try:
                    return json.loads(data)
                except:
                    continue
    return response.json()

def get_status():
    return mcp_call("agent.sessionStatus")

def post_thought(thought, prompt):
    snippet = f"[ARC Node] {prompt}\n\n{thought[:400].strip()}"
    print("  Creating text draft...")
    draft = mcp_call("create.text", {
        "prompt": snippet
    }, call_id=2)
    print(f"  Draft: {json.dumps(draft, indent=2)}")
    try:
        content = draft["result"]["content"][0]["text"]
        parsed = json.loads(content)
        short_id = parsed.get("shortId") or parsed.get("textCompletionShortId")
        if not short_id:
            return {"error": "No shortId found", "raw": parsed}
        print(f"  Publishing post: {short_id}")
        result = mcp_call("create.post", {
            "mediaShortIds": [],
            "textCompletionShortId": short_id
        }, call_id=3)
        return result
    except Exception as e:
        return {"error": str(e), "raw": draft}
