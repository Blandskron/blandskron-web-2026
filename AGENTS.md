# Instrucciones para agentes

## Propósito

Aplicación web corporativa Blandskron. Es un proyecto Django monolítico con dos aplicaciones: `landing` y `blog`.

## Lectura prioritaria

1. [`README.md`](README.md)
2. [`docs/agent/PERMISSIONS.md`](docs/agent/PERMISSIONS.md)
3. [`docs/agent/CONFIG.md`](docs/agent/CONFIG.md)
4. [`docs/agent/TESTS.md`](docs/agent/TESTS.md)
5. [`docs/agent/SECURITY.md`](docs/agent/SECURITY.md)
6. [`docs/agent/DATA_SCHEMA.md`](docs/agent/DATA_SCHEMA.md)
7. [`docs/agent/RUNBOOK.md`](docs/agent/RUNBOOK.md)

## Stack detectado

Python 3.13 en Docker, Django 6.0.1, SQLite, SMTP, WhiteNoise, Gunicorn y Docker Compose. Dependencias fijadas en `blandskron/requirements.txt`.

## Límites de cambio

Puedes modificar código, templates, estilos y documentación dentro del alcance explícito de la tarea. No expongas valores de `.env`, secretos, contraseñas, datos de contacto reales ni bases de datos locales.

Requiere aprobación humana: cambios de infraestructura o despliegue productivo, rotación o publicación de secretos, eliminación de migraciones, cambios de licencias, historial Git, permisos o volúmenes persistentes.

## Comandos reales

Desde `blandskron/`: `python manage.py migrate`, `python manage.py check`, `python manage.py collectstatic --noinput` y `python manage.py runserver`. Docker Compose define `docker compose up --build`.

## Seguridad

No imprimas secretos. Usa `example.env` solo como inventario de variables; sus valores de ejemplo no deben tratarse como seguros. Revisa [`docs/agent/SECURITY.md`](docs/agent/SECURITY.md) y [`docs/agent/CONFIG.md`](docs/agent/CONFIG.md) antes de tocar configuración.

## Validación y terminado

Antes de cerrar: ejecuta `python manage.py check`, valida enlaces Markdown y revisa el diff. Si el cambio afecta estáticos, usa `python manage.py collectstatic --noinput`; si afecta modelos, ejecuta migraciones y documenta el resultado. Una tarea está terminada cuando el cambio solicitado está implementado, las validaciones ejecutadas están reportadas y no quedan referencias a archivos inexistentes.
