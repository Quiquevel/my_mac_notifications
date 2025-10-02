import time
import json
import sys
from plyer import notification


def load_config():
    """Carga la configuración desde config.json"""
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró config.json. Usa los valores por defecto.")
        return {
            "block_minutes": 40,
            "messages": ["Descansa un poco", "Hidrátate", "Estírate"],
            "loops": 0
        }


def send_notification(title, message):
    """Manda una notificación en macOS (y multiplataforma)"""
    notification.notify(
        title=title,
        message=message,
        timeout=10  # segundos que dura la notificación
    )


def start_timer(config):
    block_minutes = config.get("block_minutes", 40)
    messages = config.get("messages", ["Descansa un poco"])
    loops = config.get("loops", 0)  # 0 = infinito

    count = 0
    while True:
        time.sleep(block_minutes * 60)  # espera el bloque de tiempo
        count += 1

        for msg in messages:
            send_notification("Recordatorio", msg)
            time.sleep(2)  # pequeño espacio entre mensajes

        if loops > 0 and count >= loops:
            print("✅ Se han completado todos los bloques configurados.")
            break


if __name__ == "__main__":
    config = load_config()
    try:
        print("⏳ Iniciando temporizador...")
        start_timer(config)
    except KeyboardInterrupt:
        print("\n🛑 Temporizador detenido por el usuario.")
        sys.exit(0)