"""Vistas públicas de la landing y páginas legales."""

import logging
import smtplib

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from .forms import ContactForm
from .services import save_contact_message

logger = logging.getLogger(__name__)


def _send_contact_emails(*, name: str, email: str, message_text: str) -> None:
    """Send the acknowledgement email and internal contact notification."""
    context = {"name": name, "message": message_text}
    html_body = render_to_string("landing/emails/contact_ack.html", context)
    text_body = render_to_string("landing/emails/contact_ack.txt", context)

    user_message = EmailMultiAlternatives(
        subject=f"{settings.EMAIL_SUBJECT_PREFIX}Recibimos tu mensaje",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        reply_to=[settings.CONTACT_NOTIFY_EMAIL],
    )
    user_message.attach_alternative(html_body, "text/html")
    user_message.send(fail_silently=False)

    owner_body = render_to_string("landing/emails/contact_notify.txt", {
        "name": name,
        "email": email,
        "message": message_text,
    })
    owner_message = EmailMultiAlternatives(
        subject=f"{settings.EMAIL_SUBJECT_PREFIX}Nuevo contacto: {name}",
        body=owner_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_NOTIFY_EMAIL],
        reply_to=[email],
    )
    owner_message.send(fail_silently=False)


def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Revisa el formulario: faltan datos o hay errores.")
            return redirect("landing:home")

        name = (form.cleaned_data.get("name") or "").strip()
        email = (form.cleaned_data.get("email") or "").strip()
        message_text = (form.cleaned_data.get("message") or "").strip()

        if form.cleaned_data.get("website"):
            messages.error(request, "No fue posible procesar el formulario.")
            return redirect("landing:home")

        contact_message = save_contact_message(
            name=name,
            email=email,
            message=message_text,
        )

        try:
            _send_contact_emails(name=name, email=email, message_text=message_text)
            messages.success(request, "¡Gracias por tu mensaje! Te contactaremos pronto.")
        except (OSError, RuntimeError, smtplib.SMTPException):
            logger.exception(
                "ERROR SMTP enviando correos de contacto (contact_message_id=%s)",
                contact_message.pk,
            )
            messages.warning(
                request,
                "Recibimos tu mensaje, pero no pudimos enviar el correo automático. Te contactaremos igual.",
            )
        return redirect("landing:home")

    return render(request, "landing/index.html", {
        "form": ContactForm(),
        "page_title": "Blandskron | Ciberseguridad, DevOps y Desarrollo de Software",
        "page_description": "Blandskron impulsa la transformación digital de empresas en Chile y LATAM con ciberseguridad, DevOps y desarrollo de software.",
    })


def privacy_policy(request):
    return render(request, "landing/legal/privacy.html", {
        "page_title": "Política de privacidad | Blandskron",
        "page_description": "Conoce cómo Blandskron trata los datos enviados mediante su sitio web.",
    })


def terms_and_conditions(request):
    return render(request, "landing/legal/terms.html", {
        "page_title": "Términos y condiciones | Blandskron",
        "page_description": "Términos y condiciones de uso del sitio web de Blandskron.",
    })


def cookies_policy(request):
    return render(request, "landing/legal/cookies.html", {
        "page_title": "Política de cookies | Blandskron",
        "page_description": "Información sobre cookies y tecnologías similares utilizadas por Blandskron.",
    })


def accessibility(request):
    return render(request, "landing/legal/accessibility.html", {
        "page_title": "Accesibilidad | Blandskron",
        "page_description": "Compromiso y canales de contacto sobre accesibilidad del sitio de Blandskron.",
    })


CAPABILITY_PAGES = {
    "desarrollo-de-software": ("Desarrollo de software", "Construcción de aplicaciones web, APIs y sistemas internos mantenibles.", "Django, FastAPI, Python, Node.js y Docker."),
    "inteligencia-artificial": ("Inteligencia artificial", "Agentes, RAG y automatización documental con contexto y controles.", "OpenAI, Anthropic, RAG, MCP y agentes."),
    "automatizacion": ("Automatización empresarial", "Integración de procesos y herramientas para reducir tareas repetitivas.", "APIs, workflows, ERP, CRM y eventos."),
    "ciberseguridad": ("Ciberseguridad", "Controles y prácticas para reducir exposición y aumentar resiliencia.", "Hardening, secure SDLC, monitoreo y controles."),
    "formacion": ("Formación técnica", "Transferencia de conocimiento mediante talleres, laboratorios y programas prácticos.", "Python, arquitectura, DevOps y seguridad."),
    "investigacion": ("Investigación y desarrollo", "Exploración de tecnologías emergentes convertidas en prototipos útiles.", "IA aplicada, Open Source y prototipado."),
}


def capability_page(request, slug):
    capability = CAPABILITY_PAGES.get(slug)
    if capability is None:
        raise Http404
    name, description, technology = capability
    return render(request, "landing/capability.html", {
        "page_title": f"{name} | Blandskron",
        "page_description": description,
        "capability_name": name,
        "capability_description": description,
        "capability_technology": technology,
    })


def maintenance(request):
    return render(request, "errors/503.html", status=503)


def offline(request):
    return render(request, "errors/offline.html")


def error_404(request, exception):
    return render(request, "errors/404.html", status=404)


def error_403(request, exception):
    return render(request, "errors/403.html", status=403)


def error_500(request):
    return render(request, "errors/500.html", status=500)


def sitemap_xml(request):
    urls = [
        "https://www.blandskron.com/",
        "https://www.blandskron.com/blog/",
        "https://www.blandskron.com/politica-de-privacidad",
        "https://www.blandskron.com/terminos-y-condiciones",
        "https://www.blandskron.com/politica-de-cookies",
        "https://www.blandskron.com/accesibilidad",
    ]
    urls.extend(
        f"https://www.blandskron.com/capacidades/{slug}"
        for slug in CAPABILITY_PAGES
    )
    body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
    body += "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    body += "</urlset>"
    return HttpResponse(body, content_type="application/xml; charset=utf-8")


def humans_txt(request):
    return HttpResponse("Blandskron SpA\nTecnología, software, automatización, IA y ciberseguridad.\nhttps://www.blandskron.com/\n", content_type="text/plain; charset=utf-8")


def security_txt(request):
    return HttpResponse("Contact: mailto:privacy@blandskron.com\nCanonical: https://www.blandskron.com/.well-known/security.txt\n", content_type="text/plain; charset=utf-8")


def robots_txt(request):
    content = """User-agent: *
Allow: /
Disallow: /blandskron-panel/

Sitemap: https://www.blandskron.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def llm_txt(request):
    content = """# Blandskron

> Sitio corporativo de Blandskron sobre tecnología, formación, innovación, desarrollo de software, DevOps y ciberseguridad.

## Sitio

- [Inicio](https://www.blandskron.com/)
- [Blog](https://www.blandskron.com/blog/)
- [Términos y condiciones](https://www.blandskron.com/terminos-y-condiciones)
- [Política de privacidad](https://www.blandskron.com/politica-de-privacidad)
- [Política de cookies](https://www.blandskron.com/politica-de-cookies)
- [Accesibilidad](https://www.blandskron.com/accesibilidad)

## Contacto

Para consultas sobre servicios o correcciones de contenido: contacto@blandskron.com.
"""
    return HttpResponse(content, content_type="text/plain; charset=utf-8")
