"""Casos de uso de la aplicación landing."""

from .models import ContactMessage


def save_contact_message(*, name: str, email: str, message: str) -> ContactMessage:
    """Persist a validated contact request before attempting SMTP delivery."""
    return ContactMessage.objects.create(
        name=name,
        email=email,
        message=message,
    )
