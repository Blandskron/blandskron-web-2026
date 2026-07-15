# Runbook local

## Ejecución local

Desde la raíz del repositorio, entra en `blandskron/`, instala `requirements.txt`, ejecuta `python manage.py migrate` y levanta `python manage.py runserver`. La configuración carga `.env` desde esa carpeta.

## Docker

`docker compose up --build --force-recreate` construye desde el Dockerfile local, expone `8000`, ejecuta `docker-entrypoint.sh`, aplica migraciones y recopila estáticos antes de arrancar Gunicorn con tres workers. El volumen persistente contiene solo `/data/db.sqlite3`; el código y los templates vienen de la imagen recién construida.

Para descartar completamente capas de build antiguas: `docker compose build --no-cache web` y luego `docker compose up -d --force-recreate web`.

## Validación y fallos frecuentes

- Configuración: `python manage.py check`.
- Base de datos: `python manage.py migrate`.
- Estáticos: `python manage.py collectstatic --noinput`.
- SMTP: revisar nombres de variables y puerto en `.env`; no registrar contraseñas.
- Host rechazado: confirmar `DJANGO_ALLOWED_HOSTS` para el entorno.

> Pendiente de confirmar: procedimiento oficial de reinicio, observabilidad, health check y proveedor de despliegue.
