import requests

# Fill these in from your BotFather + Telegram
TELEGRAM_BOT_TOKEN = "8400373852:AAHZWbbjMqV7Re0ZbjtgLOcMTJ2T1jERGbE"
TELEGRAM_CHAT_ID = "1347450785"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("⚠️ Failed to send Telegram alert:", response.text)
    except Exception as e:
        print("❌ Telegram Error:", e)
