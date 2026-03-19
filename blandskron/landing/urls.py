"""
Blandskron — Open Project

Este código forma parte de un proyecto abierto de uso profesional y educativo.
Puede ser utilizado, modificado y distribuido libremente.

Si utilizas este código en proyectos públicos o comerciales,
se agradece mantener los créditos originales.

https://blandskron.com
"""

from django.urls import path
from .views import home, privacy_policy

app_name = "landing"

urlpatterns = [
    path("", home, name="home"),
    path("privacidad/", privacy_policy, name="privacy_policy"),
]
