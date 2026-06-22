import requests

# Recibimos 'db' y 'Tarea' como parámetros desde app.py
def main(db, Tarea, app):
    print("El bot ha iniciado el proceso...")
    
    # Usamos app.app_context() para poder consultar la base de datos
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
            print("Bot enviado con éxito.")
        except Exception as e:
            print(f"Error al enviar WhatsApp: {e}")