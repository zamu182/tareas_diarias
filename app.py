import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
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

with app.app_context():
    db.create_all()
    try:
        db.session.execute(text("ALTER TABLE tarea ADD COLUMN archivada BOOLEAN DEFAULT FALSE;"))
        db.session.commit()
    except:
        db.session.rollback()

@app.route('/')
def index():
    return render_template('index.html', tareas=Tarea.query.filter_by(archivada=False).all())

@app.route('/agregar', methods=['POST'])
def agregar():
    db.session.add(Tarea(texto=request.form.get('tarea'), descripcion=request.form.get('descripcion'), 
                         fecha=request.form.get('fecha'), prioridad=request.form.get('prioridad')))
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
    return jsonify([{'title': t.texto, 'start': t.fecha, 'color': '#dc3545' if t.prioridad == 'Alta' else ('#ffc107' if t.prioridad == 'Media' else '#198754')} 
                    for t in Tarea.query.filter_by(archivada=False).all()])

if __name__ == '__main__':
    app.run()