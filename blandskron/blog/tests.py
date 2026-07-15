"""
Blandskron — Open Project

Este código forma parte de un proyecto abierto de uso profesional y educativo.
Puede ser utilizado, modificado y distribuido libremente.

Si utilizas este código en proyectos públicos o comerciales,
se agradece mantener los créditos originales.

https://blandskron.com
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post, Tag
from .templatetags.blog_filters import markdown_to_html


class BlogModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="author")

    def test_tag_generates_slug_when_missing(self):
        tag = Tag.objects.create(name="Arquitectura Cloud")

        self.assertEqual(tag.slug, "arquitectura-cloud")

    def test_post_generates_slug_when_missing(self):
        post = Post.objects.create(
            title="Buenas prácticas Django",
            author=self.author,
            content="Contenido del artículo.",
        )

        self.assertEqual(post.slug, "buenas-practicas-django")


class BlogViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="author")
        cls.security_tag = Tag.objects.create(name="Ciberseguridad")
        cls.devops_tag = Tag.objects.create(name="DevOps")
        cls.security_post = Post.objects.create(
            title="Seguridad para equipos modernos",
            author=cls.author,
            content="Buenas prácticas de ciberseguridad.",
        )
        cls.security_post.tags.add(cls.security_tag)
        cls.devops_post = Post.objects.create(
            title="Automatización con DevOps",
            author=cls.author,
            content="Pipelines y despliegues repetibles.",
        )
        cls.devops_post.tags.add(cls.devops_tag)

    def test_blog_list_renders_posts(self):
        response = self.client.get(reverse("blog:blog_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.security_post.title)
        self.assertContains(response, self.devops_post.title)

    def test_blog_search_filters_by_title_or_content(self):
        response = self.client.get(reverse("blog:blog_list"), {"q": "pipelines"})

        self.assertContains(response, self.devops_post.title)
        self.assertNotContains(response, self.security_post.title)

    def test_blog_tag_filter_returns_matching_posts(self):
        response = self.client.get(
            reverse("blog:blog_list"),
            {"tag": self.security_tag.slug},
        )

        self.assertContains(response, self.security_post.title)
        self.assertNotContains(response, self.devops_post.title)

    def test_post_detail_renders_requested_post(self):
        response = self.client.get(
            reverse("blog:post_detail", kwargs={"slug": self.security_post.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.security_post.title)
        self.assertContains(response, self.security_post.content)

    def test_missing_post_returns_not_found(self):
        response = self.client.get(
            reverse("blog:post_detail", kwargs={"slug": "does-not-exist"})
        )

        self.assertEqual(response.status_code, 404)


class MarkdownSafetyTests(TestCase):
    def test_markdown_removes_script_tags(self):
        rendered = markdown_to_html("<script>alert('xss')</script><strong>Seguro</strong>")

        self.assertNotIn("<script", rendered)
        self.assertIn("<strong>Seguro</strong>", rendered)
