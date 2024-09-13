# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo requirements.txt y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el certificado al contenedor
COPY auth.miestadofinanciero.duckdns.org.crt /usr/local/share/ca-certificates/

# Actualiza los certificados del sistema
RUN apt-get update && apt-get install -y ca-certificates && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copia el código fuente de la aplicación
COPY . .

# Expone el puerto 8080 para la aplicación
EXPOSE 8080

# Establece la variable de entorno para los certificados
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Comando para ejecutar la aplicación
CMD ["python", "-m", "app.main"]