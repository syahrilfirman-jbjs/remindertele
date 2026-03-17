import os
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import datetime
import pytz

# --- KONFIGURASI ---
TOKEN = "7815476159:AAHQYXnTpKkCvM2hqR-jP9mLoz019MzNTHI"
CHAT_ID = "-1002511736262" 
PESAN_REMINDER = "⏰ PERSIAPAN! Mohon lakukan persiapan menyanyikan lagu Indonesia Raya"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
jakarta_tz = pytz.timezone("Asia/Jakarta")

def send_reminder():
    try:
        # Mengirim pesan ke grup
        bot.send_message(CHAT_ID, PESAN_REMINDER, parse_mode="Markdown")
        print(f"[{datetime.datetime.now(jakarta_tz)}] Reminder terkirim!")
    except Exception as e:
        print(f"Gagal mengirim: {e}")

# --- PENJADWALAN (CRON) ---
scheduler = BackgroundScheduler(timezone=jakarta_tz)

# day_of_week='mon-fri' artinya Senin sampai Jumat saja
scheduler.add_job(
    send_reminder, 
    'cron', 
    day_of_week='mon-fri', 
    hour=9, 
    minute=57
)
scheduler.start()

# Endpoint Health-Check untuk Cron-job.org
@app.route('/')
def index():
    now = datetime.datetime.now(jakarta_tz)
    return f"Bot Aktif. Waktu Server (WIB): {now.strftime('%H:%M:%S')}"

if __name__ == "__main__":
    import threading
    # Jalankan Bot Polling di thread terpisah (untuk fitur command /start dll)
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    
    # Jalankan Flask Server
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
