# Usa una imagen base de Python
FROM python:3.9-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt y las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Expon el puerto en el que correrá Flask
EXPOSE 8080

# Comando para correr la aplicación
CMD ["python", "backend_falabella.py"]
