import time
import json
import sys
import subprocess
import random  # <--- para elegir mensajes aleatoriamente


def send_notification(title, message):
    """Send a native macOS notification using AppleScript"""
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])


def load_config():
    """Load configuration from config.json"""
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ config.json not found. Using default values.")
        return {
            "block_minutes": 40,
            "messages": ["Take a break", "Drink water", "Stretch"],
            "loops": 0
        }


def start_timer(config):
    block_minutes = config.get("block_minutes", 40)
    messages = config.get("messages", ["Take a break"])
    loops = config.get("loops", 0)  # 0 = infinite

    count = 0
    while True:
        time.sleep(block_minutes * 60)
        count += 1

        # Elegir un mensaje aleatorio y mostrarlo
        msg = random.choice(messages)
        send_notification("Reminder", msg)

        if loops > 0 and count >= loops:
            print("✅ All configured blocks completed.")
            break


if __name__ == "__main__":
    config = load_config()
    try:
        print("⏳ Starting timer...")
        start_timer(config)
    except KeyboardInterrupt:
        print("\n🛑 Timer stopped by user.")
        sys.exit(0)
