from django.urls import path

from .views import accessibility, capability_page, cookies_policy, home, maintenance, offline, privacy_policy, terms_and_conditions

app_name = "landing"

urlpatterns = [
    path("", home, name="home"),
    path("privacidad/", privacy_policy, name="privacy_policy_legacy"),
    path("politica-de-privacidad", privacy_policy, name="privacy_policy"),
    path("terminos-y-condiciones", terms_and_conditions, name="terms_and_conditions"),
    path("politica-de-cookies", cookies_policy, name="cookies_policy"),
    path("accesibilidad", accessibility, name="accessibility"),
    path("capacidades/<slug:slug>", capability_page, name="capability_page"),
    path("mantenimiento/", maintenance, name="maintenance"),
    path("offline/", offline, name="offline"),
]
