from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos local SQLite (creará un archivo proyectos.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proyectos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos el mapeador de la base de datos
db = SQLAlchemy(app)

# Definimos el Modelo: esto le dice a SQLite cómo estructurar la tabla
class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID único e incremental
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(50), default="En progreso")

# Contexto de Flask para generar el archivo físico de la BD si no existe
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    nombre_usuario = "Andrés"
    
    if request.method == "POST":
        nuevo_titulo = request.form.get("titulo_proyecto")
        nueva_desc = request.form.get("descripcion_proyecto")
        
        if nuevo_titulo and nueva_desc:
            # Creamos el registro usando la estructura de la clase
            nuevo_proyecto = Proyecto(titulo=nuevo_titulo, descripcion=nueva_desc)
            # Guardamos los datos de manera persistente en el disco
            db.session.add(nuevo_proyecto)
            db.session.commit()
            
        return redirect(url_for("home"))
        
    # Consultamos TODOS los registros almacenados en la tabla de SQLite
    lista_proyectos = Proyecto.query.all()
    
    return render_template("index.html", nombre=nombre_usuario, proyectos=lista_proyectos)

# RUTA: Completar Proyecto
@app.route("/completar/<int:id>")
def completar(id):
    proyecto = Proyecto.query.get_or_404(id)
    proyecto.estado = "Completado"
    db.session.commit()
    return redirect(url_for("home"))

# RUTA: Eliminar Proyecto
@app.route("/eliminar/<int:id>")
def eliminar(id):
    proyecto = Proyecto.query.get_or_404(id)
    db.session.delete(proyecto)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    # Ajustamos host="0.0.0.0" para permitir conexiones externas desde el contenedor
    app.run(host="0.0.0.0", port=5000, debug=True)