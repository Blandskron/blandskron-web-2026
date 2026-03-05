FROM python:3.13-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/blandskron

WORKDIR /app

# Instalamos dependencias del sistema (build-essential es clave para Django 6 y extensiones C)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 1. Copiamos el archivo de requerimientos desde la subcarpeta blandskron
COPY blandskron/requirements.txt /app/requirements.txt

# 2. Instalamos dependencias (Django 6.0.1 y las versiones específicas que me pasaste)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt gunicorn

# 3. Copiamos todo el contenido del proyecto al contenedor
# Esto pondrá la carpeta 'blandskron' dentro de '/app/'
COPY . /app/

# 4. Ajustamos permisos al entrypoint que está en la raíz
RUN chmod +x /app/docker-entrypoint.sh

# 5. Cambiamos el directorio de trabajo a donde está 'manage.py' 
# Según tu imagen, manage.py está dentro de la carpeta /app/blandskron/
WORKDIR /app/blandskron

EXPOSE 8000

# Usamos la ruta absoluta al script para evitar confusiones de directorio
ENTRYPOINT ["/app/docker-entrypoint.sh"]