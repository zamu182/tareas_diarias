import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Configuración Base de Datos
db_url = os.environ.get("DATABASE_URL", "sqlite:///tareas.db")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    fecha = db.Column(db.String(20), nullable=False)
    prioridad = db.Column(db.String(20))
    completo = db.Column(db.Boolean, default=False)

# Scheduler
def tarea_diaria():
    with app.app_context():
        print("Ejecutando tarea diaria...")

scheduler = BackgroundScheduler()
scheduler.add_job(tarea_diaria, 'cron', hour=8, minute=0)
scheduler.start()

# Rutas
@app.route('/')
def index():
    tareas = Tarea.query.all()
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    t = Tarea(
        texto=request.form.get('tarea'),
        descripcion=request.form.get('descripcion'),
        fecha=request.form.get('fecha'),
        prioridad=request.form.get('prioridad')
    )
    db.session.add(t)
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
    db.session.delete(Tarea.query.get(id))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/tareas')
def api_tareas():
    tareas = Tarea.query.all()
    # Colores: Alta (Rojo), Media (Naranja), Baja (Verde)
    eventos = []
    for t in tareas:
        color = '#ef4444' if t.prioridad == 'Alta' else ('#f59e0b' if t.prioridad == 'Media' else '#10b981')
        eventos.append({
            'title': t.texto,
            'start': t.fecha,
            'color': color,
            'extendedProps': {'description': t.descripcion}
        })
    return jsonify(eventos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()