"""
ASGI config for blandskron project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/

Blandskron — Open Project

Este código forma parte de un proyecto abierto de uso profesional y educativo.
Puede ser utilizado, modificado y distribuido libremente.

Si utilizas este código en proyectos públicos o comerciales,
se agradece mantener los créditos originales.

https://blandskron.com
"""


import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blandskron.settings')

application = get_asgi_application()
