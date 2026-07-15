from django.contrib import admin
from django.urls import include, path

from landing.views import (
    error_403,
    error_404,
    error_500,
    humans_txt,
    llm_txt,
    robots_txt,
    security_txt,
    sitemap_xml,
)

handler403 = "landing.views.error_403"
handler404 = "landing.views.error_404"
handler500 = "landing.views.error_500"

urlpatterns = [
    path("robots.txt", robots_txt, name="robots_txt"),
    path("llm.txt", llm_txt, name="llm_txt"),
    path("sitemap.xml", sitemap_xml, name="sitemap_xml"),
    path("humans.txt", humans_txt, name="humans_txt"),
    path(".well-known/security.txt", security_txt, name="security_txt"),
    path("blandskron-panel/", admin.site.urls),
    path("", include("landing.urls")),
    path("blog/", include("blog.urls")),
]
