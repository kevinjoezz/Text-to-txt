import sys
import json
import threading
import requests
import websocket
import time

# --- CONFIGURATION ---
TOKEN = "MTQ5Mjc3NzE3OTMyNTY2NTMzMA.GdHgYl.h3zHMB8BngOixZZj8K5TlDbWB_XSk2ksg_7Jq0"
MY_ID = "1443956898079445094"
VOUCH_CHANNEL = "<#1472476353034063993>" 
# ---------------------

P, C, G, Y, R, B, E = '\033[95m', '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[1m', '\033[0m'

target_channel = None
bot_user_id = None

def send_msg(content, channel_id, reply_to=None):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}
    payload = {"content": content}
    if reply_to:
        payload["message_reference"] = {"message_id": reply_to}
    try:
        requests.post(url, headers=headers, json=payload, timeout=5)
    except: pass

def on_message(ws, message):
    global target_channel, bot_user_id
    data = json.loads(message)
    
    # Get Bot ID on start
    if data.get('t') == 'READY':
        bot_user_id = data['d']['user']['id']

    if data.get('t') == 'MESSAGE_CREATE':
        msg = data['d']
        author_id = msg['author']['id']
        
        # 1. HYPER-SYNC
        if author_id == str(MY_ID):
            target_channel = msg['channel_id']
            sys.stdout.write(f"\r{G}⚡ ADHITHI LOCKED: {target_channel}{E}         ")
            sys.stdout.flush()

        # 2. STRICT VOUCH LOGIC
        content_lower = msg['content'].lower()
        if "working" in content_lower and author_id != str(MY_ID):
            # Check if it's a reply
            ref = msg.get('message_reference')
            if ref:
                # IMPORTANT: Fetch the message they are replying to
                ref_msg_id = ref.get('message_id')
                chan_id = msg['channel_id']
                
                # Verify who they replied to
                try:
                    r = requests.get(f"https://discord.com/api/v10/channels/{chan_id}/messages/{ref_msg_id}", 
                                     headers={"Authorization": f"Bot {TOKEN}"})
                    if r.status_code == 200:
                        original_author_id = r.json()['author']['id']
                        
                        # Only trigger if the reply is to YOU or the BOT
                        if original_author_id in [str(MY_ID), str(bot_user_id)]:
                            negatives = ["not", "n't", "dont", "don't", "no"]
                            if not any(neg in content_lower for neg in negatives):
                                reminder = f"**✧ Thank you! Don't forget to vouch in {VOUCH_CHANNEL} ✧**"
                                send_msg(reminder, chan_id, reply_to=msg['id'])
                                print(f"\n{C}✦ VALID VOUCH REPLY DETECTED ✦{E}")
                except: pass

def terminal_loop():
    global target_channel
    while True:
        lines = []
        while True:
            line = sys.stdin.readline()
            if not line or line == "\n": break
            lines.append(line.strip())
        
        content = "\n".join(lines)
        if content.strip() and target_channel:
            formatted = f"\n{content}\n"
            send_msg(formatted, target_channel)
            print(f" {P}✦ DATA DEPLOYED ✦{E}")

def run_ws():
    while True:
        try:
            ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=10&encoding=json", on_message=on_message)
            def on_open(ws):
                auth = {"op": 2, "d": {"token": TOKEN, "intents": 33280, "properties": {"os": "linux", "browser": "termux"}}}
                ws.send(json.dumps(auth))
            ws.on_open = on_open
            ws.run_forever()
        except: time.sleep(2)

if __name__ == "__main__":
    print(f"\033[95m--- ADHITHI V8 (STRICT REPLIES) ---\033[0m")
    threading.Thread(target=run_ws, daemon=True).start()
    terminal_loop()
