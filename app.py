import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

# 1. Inicialización de la aplicación
app = Flask(__name__)

# 2. Configuración de la Base de Datos
# Render usa la variable de entorno DATABASE_URL que configuraste
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de ejemplo (ajusta según lo que necesites)
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

# 3. Función para la tarea programada
def tarea_diaria():
    with app.app_context():
        print("Ejecutando tarea diaria...")
        # Importación local para evitar errores circulares
        from enviar_bot import main
        main(db, Tarea, app)

# 4. Configuración del Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(tarea_diaria, 'cron', hour=8, minute=0)
scheduler.start()

# 5. Ruta básica para que Render sepa que la app está viva
@app.route('/')
def index():
    return "El bot de tareas está activo y funcionando."

if __name__ == '__main__':
    app.run()