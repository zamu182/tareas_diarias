# 1. Usamos una imagen ligera oficial de Python como base
FROM python:3.10-slim

# 2. Definimos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de requerimientos al contenedor
COPY requirements.txt requirements.txt

# 4. Instalamos las librerías dentro del entorno aislado
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto de los archivos del proyecto a la carpeta /app
COPY . .

# 6. Exponemos el puerto 5000 que usa Flask
EXPOSE 5000

# 7. Comando para arrancar la aplicación apuntando al host global
CMD ["python", "app.py"]