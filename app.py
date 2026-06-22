import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tareas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Tarea actualizado con los campos de tu HTML
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(500))
    fecha = db.Column(db.String(20))
    prioridad = db.Column(db.String(20))
    completo = db.Column(db.Boolean, default=False)

# Rutas
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
    tarea = Tarea.query.get_or_404(id)
    tarea.completo = not tarea.completo
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for('index'))

# API para el Calendario
@app.route('/api/tareas')
def api_tareas():
    tareas = Tarea.query.all()
    eventos = [{
        'title': t.texto,
        'start': t.fecha,
        'extendedProps': {'description': t.descripcion}
    } for t in tareas]
    return jsonify(eventos)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)