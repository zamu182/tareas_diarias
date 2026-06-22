import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

# 1. Inicialización de la aplicación
app = Flask(__name__)

# 2. Configuración de la Base de Datos
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Tarea
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

# 5. Ruta para mostrar el calendario (index.html)
@app.route('/')
def index():
    # Esto busca index.html dentro de la carpeta 'templates'
    return render_template('index.html')

if __name__ == '__main__':
    app.run()