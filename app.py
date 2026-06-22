from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import enviar_bot  # Importa tu archivo enviar_bot.py

app = Flask(__name__)

# --- CONFIGURACIÓN DEL BOT AUTOMÁTICO ---
def tarea_diaria():
    print("Ejecutando el bot de WhatsApp...")
    # Llamamos a la función principal de tu script
    enviar_bot.main() 

# Configuramos el planificador
scheduler = BackgroundScheduler()
# Programa la tarea para las 08:00 AM todos los días
scheduler.add_job(tarea_diaria, 'cron', hour=8, minute=0)
scheduler.start()
# ----------------------------------------

# ... (Aquí va el resto de tu código de Flask como siempre)

if __name__ == '__main__':
    app.run()