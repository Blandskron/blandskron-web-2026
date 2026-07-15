# Permisos para agentes

## Permitido sin aprobación adicional

- Leer el código, templates, migraciones y documentación del repositorio.
- Modificar documentación y código dentro del alcance explícito de la tarea.
- Ejecutar validaciones locales no destructivas como `python manage.py check`.
- Crear archivos de trabajo ignorados, siempre que no contengan secretos.

## Protegido o sensible

- `.env`, bases SQLite (`db.sqlite3`), logs y cualquier exportación de datos.
- `blandskron/*/migrations/`, `Dockerfile`, `docker-compose.yml`, `docker-entrypoint.sh` y configuración de despliegue cuando el cambio no sea parte de la tarea.
- Secretos SMTP, claves Django, credenciales de superusuario y datos enviados por usuarios.

## Requiere aprobación humana

Desplegar, publicar imágenes, cambiar infraestructura o volúmenes, eliminar migraciones o documentos históricos, modificar licencias, rotar secretos o ejecutar operaciones destructivas sobre datos.

## Prohibido

Cometer secretos, imprimir valores de `.env`, borrar pruebas para hacer pasar una validación o afirmar que un servicio externo fue probado sin evidencia.

Si falta contexto crítico, marca `> Pendiente de confirmar: ...` y pide ayuda antes de ampliar el alcance.
