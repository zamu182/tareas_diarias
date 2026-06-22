import requests
import os
from app import app, db, Tarea

def enviar_resumen():
    with app.app_context():
        # Buscamos tareas que no estén completas
        pendientes = Tarea.query.filter_by(completo=False).all()
        
        if not pendientes:
            mensaje = "¡Hola! No tienes tareas pendientes para hoy."
        else:
            lista = "\n".join([f"- {t.texto}" for t in pendientes])
            mensaje = f"Hola, tus tareas pendientes hoy son:\n{lista}"
        
        # Datos del Bot
        api_key = "9409150"
        usuario = "+573108106671"
        
        url = "https://api.callmebot.com/whatsapp.php"
        params = {
            'phone': usuario,
            'text': mensaje,
            'apikey': api_key
        }
        
        try:
            requests.get(url, params=params)
            print("Bot ejecutado con éxito.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    enviar_resumen()