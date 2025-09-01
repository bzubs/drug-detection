# -------- Configure Gemini API Key --------
GOOGLE_API_KEY = 'AIzaSyAL_jbXYAyDAHLuiYvdsd1DRBUSMqieCcY'

import re
import asyncio
from telethon import TelegramClient, events
from google import genai
import os

# -------- Google Gemini Setup --------
if not GOOGLE_API_KEY:
    raise SystemExit("Set the GOOGLE_API_KEY environment variable first!")

gemini_client = genai.Client(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# -------- Telegram Setup --------
api_id = 25333298
api_hash = 'aca9a860499b58236bebe585ecf18caf'
phone = '+919545511731'
group_link = "https://t.me/+20kr1VpDj3BmMDU1"
severity_threshold = 6.0

client = TelegramClient('session', api_id, api_hash)

# -------- System Prompt --------
SYSTEM_PROMPT = """
You are an AI safety classifier.
Analyze a chat message and detect:
- Drug abuse (including slang like coke, weed, mdma)
- Illicit substance use
- Buying/selling of drugs
- Any illegal substance-related activity

Return a single severity number 0-10:
0-2: Harmless
3-5: Mild mention
6-8: Strong suspicion
9-10: Explicit illegal activity

Output ONLY the number (e.g. 0, 3.5, 9).
"""

# -------- Function to get severity from Gemini --------
def get_severity(message: str) -> float:
    prompt = f"{SYSTEM_PROMPT}\nMessage: \"{message.strip()}\""
    response = gemini_client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    text = response.text
    match = re.search(r"\d+(\.\d+)?", text)
    if match:
        try:
            return float(match.group())
        except:
            return 0.0
    return 0.0

# -------- Event Handler for New Messages (Dev Mode) --------
@client.on(events.NewMessage(chats=group_link))
async def handler(event):
    msg = event.message.message
    sender = await event.get_sender()
    sender_name = getattr(sender, "username", getattr(sender, "first_name", str(sender.id)))

    # --- Dev filter: only process messages containing 'test' ---
    if "test" not in msg.lower():
        return

    severity = get_severity(msg)
    log_entry = f"[{sender_name}] Severity: {severity} | Message: {msg}\n"
    print(log_entry)

    # --- Log to dev file ---
    with open("dev_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

    if severity >= severity_threshold:
        alert_msg = f"🚨 High-risk message detected!\nSeverity: {severity}\nContent: {msg} \n Pls Click on this link https://71db938084ff.ngrok-free.app"
        await client.send_message(group_link, alert_msg)
        print("✅ Alert sent!")

# -------- Run Client --------
async def main():
    await client.start(phone)
    print("✅ Dev monitoring started. Only messages with 'test' are scored.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
