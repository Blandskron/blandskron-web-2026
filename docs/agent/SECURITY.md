# Seguridad

## Secretos y datos sensibles

`.env` está ignorado por Git y contiene configuración sensible. Nunca lo copies a documentación, logs, issues o commits. Usa `example.env` como referencia, pero reemplaza todos sus valores de ejemplo antes de usarlo.

La aplicación recibe mensajes de contacto y los guarda en SQLite; después envía un acuse al usuario y una notificación interna por SMTP. Trata nombre, correo y mensaje como datos personales.

## Configuración peligrosa detectada

`settings.py` tiene una clave Django fallback para desarrollo y activa `DEBUG` si no se configura la variable correspondiente. No uses esos defaults en producción. Configura `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` y `DJANGO_ALLOWED_HOSTS` explícitamente.

El entrypoint puede crear un superusuario si recibe `DJANGO_SUPERUSER_USERNAME` y `DJANGO_SUPERUSER_PASSWORD`. No documentes ni compartas esos valores.

## Límites operativos

No cambies rutas administrativas, SMTP, persistencia Docker o configuración productiva sin revisar el impacto. No presentes datos reales de la base de datos durante diagnósticos.

> Pendiente de confirmar: política de retención y borrado de mensajes de contacto, controles de acceso al panel y gestión de copias de seguridad.
