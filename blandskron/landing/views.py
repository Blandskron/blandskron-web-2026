from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ContactForm

def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Aquí tú defines qué hacer:
            # - enviar correo (send_mail)
            # - guardar en DB
            # - enviar a CRM, etc.
            messages.success(request, "¡Gracias por tu mensaje! Te contactaré pronto.")
            return redirect("landing:home")
        else:
            messages.error(request, "Revisa el formulario: faltan datos o hay errores.")
    else:
        form = ContactForm()

    return render(request, "landing/index.html", {"form": form})
