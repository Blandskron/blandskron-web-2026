# Configuración

La configuración se carga desde `.env` ubicado junto a `manage.py` y desde variables del entorno del contenedor. `.env` no debe versionarse.

Variables confirmadas por el código y el entrypoint:

- Django: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`.
- SMTP: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_SSL`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`, `EMAIL_SUBJECT_PREFIX`, `EMAIL_TIMEOUT`, `CONTACT_NOTIFY_EMAIL`.
- Superusuario opcional: `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`.

El puerto SMTP `465` fuerza SSL y desactiva TLS; otros puertos usan los flags configurados. La base de datos es SQLite; localmente usa `blandskron/db.sqlite3` y Docker configura `DJANGO_DB_PATH=/data/db.sqlite3` para persistir solo los datos. Los estáticos se sirven desde `STATIC_ROOT` usando WhiteNoise.

Valida la configuración sin imprimir valores con `cd blandskron; python manage.py check`.

> Pendiente de confirmar: valores requeridos por entorno, perfiles diferenciados local/staging/producción y configuración oficial de dominio.
