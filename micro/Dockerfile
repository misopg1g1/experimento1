# Selecciona la imagen base de Python
FROM python:3.9

# Copia los archivos de la aplicación a la imagen Docker
COPY . /app

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias de Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expone el puerto 80 para la aplicación
EXPOSE 8001

# Inicia la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]