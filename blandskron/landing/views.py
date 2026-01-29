"""
Blandskron — Open Project

Este código forma parte de un proyecto abierto de uso profesional y educativo.
Puede ser utilizado, modificado y distribuido libremente.

Si utilizas este código en proyectos públicos o comerciales,
se agradece mantener los créditos originales.

https://blandskron.com
"""

import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from .forms import ContactForm
from .models import ContactMessage

logger = logging.getLogger(__name__)


def _send_contact_emails(*, name: str, email: str, message_text: str) -> None:
    """
    Envía:
    1) Acuse de recibo al usuario (HTML + TXT)
    2) Notificación interna al owner (TXT)
    """
    # 1) Email al usuario (acuse)
    subject_user = f"{settings.EMAIL_SUBJECT_PREFIX}Recibimos tu mensaje"

    context = {"name": name, "message": message_text}

    html_body = render_to_string("landing/emails/contact_ack.html", context)
    text_body = render_to_string("landing/emails/contact_ack.txt", context)

    msg_user = EmailMultiAlternatives(
        subject=subject_user,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        # Si el usuario responde el acuse, te llega a ti:
        reply_to=[settings.CONTACT_NOTIFY_EMAIL],
    )
    msg_user.attach_alternative(html_body, "text/html")
    msg_user.send(fail_silently=False)

    # 2) Email interno (notificación a tu correo)
    subject_owner = f"{settings.EMAIL_SUBJECT_PREFIX}Nuevo contacto: {name}"
    owner_body = render_to_string("landing/emails/contact_notify.txt", {
        "name": name,
        "email": email,
        "message": message_text,
    })

    msg_owner = EmailMultiAlternatives(
        subject=subject_owner,
        body=owner_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_NOTIFY_EMAIL],
        # Si tú respondes este correo, responde al cliente:
        reply_to=[email],
    )
    msg_owner.send(fail_silently=False)


def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Revisa el formulario: faltan datos o hay errores.")
            return redirect("landing:home")

        name: str = (form.cleaned_data.get("name") or "").strip()
        email: str = (form.cleaned_data.get("email") or "").strip()
        message_text: str = (form.cleaned_data.get("message") or "").strip()

        # 1) Guardar en DB SIEMPRE (aunque el correo falle)
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text,
        )

        # 2) Enviar correos
        try:
            _send_contact_emails(name=name, email=email, message_text=message_text)
            messages.success(request, "¡Gracias por tu mensaje! Te contactaremos pronto.")
        except Exception:
            # Log profesional (stacktrace incluido)
            logger.exception("ERROR SMTP enviando correos de contacto (name=%s, email=%s)", name, email)

            # Mensaje simple al usuario
            messages.warning(
                request,
                "Recibimos tu mensaje, pero no pudimos enviar el correo automático. Te contactaremos igual."
            )

        return redirect("landing:home")

    # GET
    form = ContactForm()
    return render(request, "landing/index.html", {"form": form})
