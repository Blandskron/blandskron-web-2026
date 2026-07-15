"""
Blandskron — Open Project

Este código forma parte de un proyecto abierto de uso profesional y educativo.
Puede ser utilizado, modificado y distribuido libremente.

Si utilizas este código en proyectos públicos o comerciales,
se agradece mantener los créditos originales.

https://blandskron.com
"""

from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .forms import ContactForm
from .models import ContactMessage
from .views import _send_contact_emails


class ContactFormTests(TestCase):
    def test_accepts_complete_contact_data(self):
        form = ContactForm(
            data={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "message": "Necesito orientación tecnológica.",
                "privacy_accepted": True,
            }
        )

        self.assertTrue(form.is_valid())

    def test_requires_privacy_acceptance(self):
        form = ContactForm(
            data={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "message": "Necesito orientación tecnológica.",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("privacy_accepted", form.errors)


class LandingViewTests(TestCase):
    def test_home_renders(self):
        response = self.client.get(reverse("landing:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/index.html")
        self.assertContains(response, "Ciberseguridad")

    @patch("landing.views._send_contact_emails")
    def test_valid_contact_is_saved_and_emails_are_sent(self, send_emails):
        response = self.client.post(
            reverse("landing:home"),
            data={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "message": "Necesito orientación tecnológica.",
                "privacy_accepted": "on",
            },
        )

        self.assertRedirects(response, reverse("landing:home"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.get().email, "ada@example.com")
        send_emails.assert_called_once_with(
            name="Ada Lovelace",
            email="ada@example.com",
            message_text="Necesito orientación tecnológica.",
        )

    @patch("landing.views._send_contact_emails")
    def test_invalid_contact_is_not_saved_or_sent(self, send_emails):
        response = self.client.post(
            reverse("landing:home"),
            data={
                "name": "Ada Lovelace",
                "email": "not-an-email",
                "message": "Mensaje inválido.",
            },
        )

        self.assertRedirects(response, reverse("landing:home"))
        self.assertEqual(ContactMessage.objects.count(), 0)
        send_emails.assert_not_called()

    @patch("landing.views._send_contact_emails", side_effect=RuntimeError("SMTP unavailable"))
    def test_contact_remains_saved_when_email_delivery_fails(self, send_emails):
        response = self.client.post(
            reverse("landing:home"),
            data={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "message": "El correo puede fallar, pero el mensaje debe persistir.",
                "privacy_accepted": "on",
            },
        )

        self.assertRedirects(response, reverse("landing:home"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        send_emails.assert_called_once()


class ContactEmailTests(TestCase):
    @patch("landing.views.EmailMultiAlternatives")
    def test_contact_email_helper_sends_acknowledgement_and_notification(self, email_message):
        _send_contact_emails(
            name="Ada Lovelace",
            email="ada@example.com",
            message_text="Consulta de prueba.",
        )

        self.assertEqual(email_message.call_count, 2)
        self.assertEqual(email_message.return_value.send.call_count, 2)
        email_message.return_value.attach_alternative.assert_called_once()


class PublicTextAndLegalRouteTests(TestCase):
    def test_public_legal_pages_render(self):
        routes_and_markers = (
            ("landing:privacy_policy", "Política de privacidad"),
            ("landing:terms_and_conditions", "Términos y condiciones"),
            ("landing:cookies_policy", "Política de cookies"),
            ("landing:accessibility", "Accesibilidad"),
        )

        for route_name, marker in routes_and_markers:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, marker)

    def test_legacy_privacy_route_remains_available(self):
        response = self.client.get(reverse("landing:privacy_policy_legacy"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Política de privacidad")

    def test_robots_and_llm_files_are_public_text(self):
        robots = self.client.get(reverse("robots_txt"))
        llm = self.client.get(reverse("llm_txt"))

        self.assertEqual(robots.status_code, 200)
        self.assertEqual(llm.status_code, 200)
        self.assertIn("Disallow: /blandskron-panel/", robots.content.decode())
        self.assertIn("# Blandskron", llm.content.decode())
