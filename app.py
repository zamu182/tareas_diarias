from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'tareas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(500))
    fecha = db.Column(db.String(50), nullable=False)
    prioridad = db.Column(db.String(20), nullable=False)
    completo = db.Column(db.Boolean, default=False)

with app.app_context():
    if not os.path.exists(os.path.join(basedir, 'instance')):
        os.makedirs(os.path.join(basedir, 'instance'))
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', tareas=Tarea.query.all())

@app.route('/agregar', methods=['POST'])
def agregar():
    nueva = Tarea(
        texto=request.form['tarea'],
        descripcion=request.form['descripcion'],
        fecha=request.form['fecha'],
        prioridad=request.form['prioridad']
    )
    db.session.add(nueva)
    db.session.commit()
    return redirect('/')

@app.route('/check/<int:id>')
def check(id):
    t = Tarea.query.get(id)
    t.completo = not t.completo
    db.session.commit()
    return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    db.session.delete(Tarea.query.get(id))
    db.session.commit()
    return redirect('/')

@app.route('/api/tareas')
def api_tareas():
    eventos = []
    for t in Tarea.query.all():
        # Gris si está completa, color de prioridad si no
        color = '#64748b' if t.completo else ('#ef4444' if t.prioridad == 'Alta' else ('#f59e0b' if t.prioridad == 'Media' else '#10b981'))
        eventos.append({
            'id': t.id,
            'title': f"[{t.prioridad}] {t.texto}",
            'start': t.fecha,
            'backgroundColor': color,
            'extendedProps': {'description': t.descripcion or "Sin descripción"}
        })
    return jsonify(eventos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)