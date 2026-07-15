# ADR-001: Monolito modular Django

## Estado

Aceptado.

## Contexto

El repositorio contiene una aplicación Django única con dos aplicaciones de dominio:
`landing` y `blog`. Ambas se despliegan juntas mediante una imagen Docker y Gunicorn.

## Decisión

Mantener un monolito modular Django mientras el sitio conserve su alcance corporativo
actual. Cada aplicación mantiene sus modelos, URLs, vistas, administración y tests.
Los casos de uso que combinen persistencia y servicios externos se ubicarán en
`services.py` o en un paquete `services/` dentro de la aplicación correspondiente.

El flujo de contacto utiliza `landing/services.py` para persistir el mensaje antes de
intentar el envío SMTP. El envío continúa siendo síncrono hasta que exista una
necesidad operativa demostrable de incorporar una cola.

## Consecuencias

- Se conserva una estructura simple y fácil de desplegar.
- Los límites entre `landing` y `blog` permanecen claros.
- La persistencia y la presentación pueden probarse con menor acoplamiento.
- SQLite y SMTP síncrono siguen siendo decisiones adecuadas para el alcance actual,
  pero deben revisarse si aumentan el tráfico o el volumen de contactos.

## Revisión futura

Revisar esta decisión al incorporar más dominios, múltiples instancias con alta
concurrencia, procesamiento asíncrono o necesidades de escalabilidad de base de datos.

## Organización de templates

- `templates/base.html`: layout global.
- `templates/partials/`: head y scripts compartidos.
- `templates/landing/`: landing, legales, capacidades y partials visuales.
- `templates/blog/`: listado y detalle editorial.
- `templates/errors/`: respuestas 403, 404, 500 y 503.
- `templates/errors/offline.html`: pantalla independiente para pérdida de conexión.

`templates/landing/base.html` se conserva como compatibilidad para templates antiguos;
el layout activo es `templates/base.html`.
