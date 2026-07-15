# blandskron-web-2026

Sitio web corporativo de Blandskron, construido con Django. Publica la landing
principal, un formulario de contacto, páginas legales, capacidades de servicio
y un blog administrable.

## Inicio rápido

Requisitos confirmados por el repositorio: Python 3.13 para la imagen Docker y
dependencias fijadas en [`blandskron/requirements.txt`](blandskron/requirements.txt).
Para ejecutar localmente:

```powershell
cd blandskron
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

La aplicación queda disponible en `http://127.0.0.1:8000/`. Para el flujo Docker,
prepara un `.env` local a partir de [`example.env`](example.env), sin conservar
credenciales reales en el repositorio, y ejecuta:

```powershell
docker compose up --build --force-recreate
```

El contenedor aplica migraciones, recopila estáticos y arranca Gunicorn en el
puerto `8000` mediante [`docker-entrypoint.sh`](docker-entrypoint.sh). SQLite se
persiste en un volumen separado.

## Arquitectura y organización

- `blandskron/blandskron/`: configuración, URLs y entradas WSGI/ASGI.
- `blandskron/landing/`: portada, contacto, legales y capacidades.
- `blandskron/blog/`: posts y etiquetas, accesibles bajo `/blog/`.
- `blandskron/templates/base.html`: layout global compartido.
- `blandskron/templates/partials/`: head y scripts globales.
- `blandskron/templates/landing/partials/`: secciones visuales de la landing.
- `blandskron/templates/landing/legal/`: términos, privacidad, cookies y accesibilidad.
- `blandskron/templates/errors/`: respuestas 403, 404, 500, 503 y pantalla offline.
- `blandskron/static/`: CSS, JavaScript e imágenes del sitio.
- `docs/architecture/`: decisiones arquitectónicas.
- `docs/agent/`: instrucciones operativas especializadas.

La estructura se mantiene como un monolito modular Django: cada aplicación
conserva sus modelos, URLs, vistas, administración y tests. Consulta
[`docs/architecture/ADR-001-monolito-django.md`](docs/architecture/ADR-001-monolito-django.md)
para el detalle de la decisión.

## Rutas públicas

- `/`
- `/blog/` y `/blog/<slug>/`
- `/terminos-y-condiciones`
- `/politica-de-privacidad`
- `/politica-de-cookies`
- `/accesibilidad`
- `/capacidades/<slug>`
- `/robots.txt`, `/llm.txt`, `/sitemap.xml`, `/humans.txt`
- `/.well-known/security.txt`

El panel de administración está en `/blandskron-panel/`. Las rutas de operación
`/mantenimiento/` y `/offline/` utilizan plantillas bajo `templates/errors/`.

## Agentes y contribución

Los agentes deben leer [`AGENTS.md`](AGENTS.md) antes de modificar el proyecto.
Las reglas de permisos, configuración, seguridad, operación, pruebas y datos están
en [`docs/agent/`](docs/agent/).

Antes de cerrar un cambio, ejecuta las validaciones indicadas en
[`docs/agent/TESTS.md`](docs/agent/TESTS.md) y declara cualquier validación
pendiente.

> Pendiente de confirmar: proveedor de despliegue, proceso de publicación de la
> imagen `blandskron/portafolioweb:latest` y política de copias de seguridad de SQLite.
