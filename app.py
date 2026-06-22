from apscheduler.schedulers.background import BackgroundScheduler
from enviar_bot import main  # Importamos la función limpia

# ... (arriba ya tienes tu app, db y Tarea definidos)

def tarea_diaria():
    print("Llamando al bot desde el scheduler...")
    # Pasamos db, Tarea y también app para el contexto
    main(db, Tarea, app) 

scheduler = BackgroundScheduler()
scheduler.add_job(tarea_diaria, 'cron', hour=8, minute=0)
scheduler.start()