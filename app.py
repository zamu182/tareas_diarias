import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

# 1. Inicialización
app = Flask(__name__)

# 2. Configuración Base de Datos
db_url = os.environ.get("DATABASE_URL", "sqlite:///tareas.db")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo actualizado para coincidir con tu HTML
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(100), nullable=False) # name="tarea" en HTML
    descripcion = db.Column(db.String(200))
    fecha = db.Column(db.String(20), nullable=False) # name="fecha" en HTML
    prioridad = db.Column(db.String(20))
    completo = db.Column(db.Boolean, default=False)

# 3. Scheduler
def tarea_diaria():
    with app.app_context():
        print("Ejecutando tarea diaria...")
        # Asegúrate de que enviar_bot.py exista y sea compatible
        # from enviar_bot import main
        # main(db, Tarea, app)

scheduler = BackgroundScheduler()
scheduler.add_job(tarea_diaria, 'cron', hour=8, minute=0)
scheduler.start()

# 4. Rutas
@app.route('/')
def index():
    tareas = Tarea.query.all()
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    nueva_tarea = Tarea(
        texto=request.form.get('tarea'),
        descripcion=request.form.get('descripcion'),
        fecha=request.form.get('fecha'),
        prioridad=request.form.get('prioridad')
    )
    db.session.add(nueva_tarea)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/check/<int:id>')
def check(id):
    t = Tarea.query.get(id)
    t.completo = not t.completo
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    t = Tarea.query.get(id)
    if t:
        db.session.delete(t)
        db.session.commit()
    return redirect(url_for('index'))

# API para FullCalendar
@app.route('/api/tareas')
def api_tareas():
    tareas = Tarea.query.all()
    eventos = [{
        'title': t.texto,
        'start': t.fecha,
        'extendedProps': {'description': t.descripcion}
    } for t in tareas]
    return jsonify(eventos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()