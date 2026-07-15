# Pruebas y validación

El proyecto usa el runner integrado de Django; no se detectó pytest ni una herramienta externa de cobertura. Actualmente existen tests unitarios y tests de integración en las aplicaciones `landing` y `blog`.

Para ejecutar la suite completa dentro del entorno Docker reproducible:

```powershell
docker-compose run --rm --no-deps --entrypoint python web manage.py test
```

La validación mínima confirmada por Django es:

```powershell
cd blandskron
python manage.py check
python manage.py migrate --check
```

Los tests de `landing/tests.py` y `blog/tests.py` cubren lógica de formularios, modelos y vistas. Los archivos `test_integration.py` cubren flujos HTTP con templates y SQLite temporal. Para cambios en modelos o migraciones, valida migraciones; para estáticos, ejecuta `python manage.py collectstatic --noinput`; para cambios visuales, realiza una comprobación manual con el servidor local.

SMTP se mockea en tests; no se conecta a servicios externos ni usa credenciales reales.

No elimines, omitas ni relajes pruebas para forzar un resultado exitoso. Si una validación no puede ejecutarse por dependencias o servicios externos, reporta el bloqueo exacto.
