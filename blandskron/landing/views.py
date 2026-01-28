import traceback

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from .forms import ContactForm
from .models import ContactMessage


def _send_contact_emails(*, name: str, email: str, message_text: str) -> None:
    # 1) Email al usuario (acuse)
    subject_user = f"{settings.EMAIL_SUBJECT_PREFIX}Recibimos tu mensaje"

    html_body = render_to_string("landing/emails/contact_ack.html", {
        "name": name,
        "message": message_text,
    })
    text_body = render_to_string("landing/emails/contact_ack.txt", {
        "name": name,
        "message": message_text,
    })

    msg_user = EmailMultiAlternatives(
        subject=subject_user,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
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
        reply_to=[email],
    )
    msg_owner.send(fail_silently=False)


def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            email = form.cleaned_data["email"].strip()
            message_text = form.cleaned_data["message"].strip()

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
            except Exception as e:
                # Deja registro del error en consola para debug
                print("ERROR SMTP:", e)
                traceback.print_exc()

                # Pero al usuario le dices algo simple
                messages.warning(
                    request,
                    "Recibimos tu mensaje, pero no pudimos enviar el correo automático. Te contactaremos igual."
                )

            return redirect("landing:home")

        messages.error(request, "Revisa el formulario: faltan datos o hay errores.")
        return redirect("landing:home")

    # GET
    form = ContactForm()
    return render(request, "landing/index.html", {"form": form})
