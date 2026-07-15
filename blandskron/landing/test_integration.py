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

from .models import ContactMessage


class ContactFlowIntegrationTests(TestCase):
    @patch("landing.views._send_contact_emails")
    def test_contact_request_reaches_view_and_persists_message(self, send_emails):
        response = self.client.post(
            reverse("landing:home"),
            data={
                "name": "Integration User",
                "email": "integration@example.com",
                "message": "Mensaje ficticio de integración.",
                "privacy_accepted": "on",
            },
        )

        self.assertRedirects(response, reverse("landing:home"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        message = ContactMessage.objects.get()
        self.assertEqual(message.name, "Integration User")
        self.assertEqual(message.email, "integration@example.com")
        send_emails.assert_called_once_with(
            name="Integration User",
            email="integration@example.com",
            message_text="Mensaje ficticio de integración.",
        )

    @patch("landing.views._send_contact_emails", side_effect=RuntimeError("SMTP unavailable"))
    def test_contact_request_keeps_database_record_when_smtp_fails(self, send_emails):
        response = self.client.post(
            reverse("landing:home"),
            data={
                "name": "Integration User",
                "email": "integration@example.com",
                "message": "El mensaje ficticio debe persistir.",
                "privacy_accepted": "on",
            },
        )

        self.assertRedirects(response, reverse("landing:home"))
        self.assertTrue(ContactMessage.objects.filter(email="integration@example.com").exists())
        send_emails.assert_called_once()


class PublicPagesIntegrationTests(TestCase):
    def test_public_pages_resolve_through_root_urlconf(self):
        routes = (
            ("landing:home", "landing/index.html"),
            ("landing:privacy_policy", "landing/legal/privacy.html"),
            ("landing:terms_and_conditions", "landing/legal/terms.html"),
            ("landing:cookies_policy", "landing/legal/cookies.html"),
            ("landing:accessibility", "landing/legal/accessibility.html"),
        )

        for route_name, template_name in routes:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)

    def test_machine_readable_public_files_are_reachable(self):
        robots = self.client.get(reverse("robots_txt"))
        llm = self.client.get(reverse("llm_txt"))

        self.assertEqual(robots.status_code, 200)
        self.assertEqual(robots["Content-Type"], "text/plain; charset=utf-8")
        self.assertIn("Disallow: /blandskron-panel/", robots.content.decode())
        self.assertEqual(llm.status_code, 200)
        self.assertIn("# Blandskron", llm.content.decode())

    def test_error_and_operational_pages_use_the_errors_namespace(self):
        cases = (
            ("/ruta-inexistente/", 404, "errors/404.html"),
            (reverse("landing:maintenance"), 503, "errors/503.html"),
            (reverse("landing:offline"), 200, "errors/offline.html"),
        )

        for path, status_code, template_name in cases:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, status_code)
                self.assertTemplateUsed(response, template_name)
