import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Usamos una base de datos local para desarrollo/pruebas si no hay variable de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///tareas.db").replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    fecha = db.Column(db.String(20), nullable=False)
    prioridad = db.Column(db.String(20))
    completo = db.Column(db.Boolean, default=False)
    archivada = db.Column(db.Boolean, default=False)

# Crear base de datos al arrancar
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tareas = Tarea.query.filter_by(archivada=False).all()
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    try:
        nueva_tarea = Tarea(
            texto=request.form.get('tarea'),
            descripcion=request.form.get('descripcion'),
            fecha=request.form.get('fecha'),
            prioridad=request.form.get('prioridad')
        )
        db.session.add(nueva_tarea)
        db.session.commit()
    except Exception as e:
        print(f"Error al agregar: {e}")
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
    tareas_archivadas = Tarea.query.filter_by(archivada=True).all()
    return render_template('archivo.html', tareas=tareas_archivadas)

@app.route('/api/tareas')
def api_tareas():
    tareas = Tarea.query.filter_by(archivada=False).all()
    eventos = [{
        'title': t.texto, 'start': t.fecha,
        'color': '#f43f5e' if t.prioridad == 'Alta' else ('#fbbf24' if t.prioridad == 'Media' else '#10b981')
    } for t in tareas]
    return jsonify(eventos)

if __name__ == '__main__':
    app.run(debug=True)