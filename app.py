import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
# Configuración
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///tareas.db").replace("postgres://", "postgresql://", 1)
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
    archivada = db.Column(db.Boolean, default=False)

# Migración de emergencia: agrega la columna si falta
with app.app_context():
    db.create_all()
    try:
        # Intenta agregar la columna si no existe
        db.session.execute(text("ALTER TABLE tarea ADD COLUMN archivada BOOLEAN DEFAULT FALSE;"))
        db.session.commit()
    except Exception:
        db.session.rollback() # La columna ya existe, todo está bien

@app.route('/')
def index():
    return render_template('index.html', tareas=Tarea.query.filter_by(archivada=False).all())

@app.route('/agregar', methods=['POST'])
def agregar():
    db.session.add(Tarea(
        texto=request.form.get('tarea'), 
        descripcion=request.form.get('descripcion'), 
        fecha=request.form.get('fecha'), 
        prioridad=request.form.get('prioridad')
    ))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/check/<int:id>')
def check(id):
    t = Tarea.query.get(id)
    if t:
        t.completo = not t.completo
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/archivar/<int:id>')
def archivar(id):
    t = Tarea.query.get(id)
    if t:
        t.archivada = True
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/archivo')
def ver_archivo():
    return render_template('archivo.html', tareas=Tarea.query.filter_by(archivada=True).all())

@app.route('/api/tareas')
def api_tareas():
    return jsonify([{
        'title': t.texto, 'start': t.fecha,
        'color': '#f43f5e' if t.prioridad == 'Alta' else ('#fbbf24' if t.prioridad == 'Media' else '#10b981')
    } for t in Tarea.query.filter_by(archivada=False).all()])

if __name__ == '__main__':
    app.run()