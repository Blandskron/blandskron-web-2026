# Datos y contratos

## Entidades

- `landing.ContactMessage`: `name` (120), `email`, `message`, `created_at`. Se crea al enviar el formulario de contacto, incluso si el SMTP falla.
- `blog.Tag`: `name` único (50) y `slug` único, generado desde el nombre cuando falta.
- `blog.Post`: `title` (200), `slug` único, `content` en Markdown, `author` hacia el usuario Django, fechas de creación/actualización y etiquetas opcionales.

## Rutas confirmadas

- `GET /politica-de-privacidad`: política de privacidad.
- `GET /terminos-y-condiciones`: términos y condiciones.
- `GET /politica-de-cookies`: política de cookies.
- `GET /accesibilidad`: declaración de accesibilidad.

- `GET /`: landing; `POST /`: valida y persiste `ContactMessage`, luego intenta enviar dos correos.
- `GET /privacidad/`: política de privacidad.
- `GET /blog/`: lista, búsqueda por `q` y filtro por `tag`.
- `GET /blog/<slug>/`: detalle de un post.
- `/blandskron-panel/`: administración Django.

Las migraciones iniciales están en `blandskron/landing/migrations/0001_initial.py` y `blandskron/blog/migrations/0001_initial.py`. No edites migraciones aplicadas para corregir modelos: crea una nueva migración y valida compatibilidad.

> Pendiente de confirmar: contrato público de la API (no se detectó una API JSON), política de versionado de contenido y retención de `ContactMessage`.
