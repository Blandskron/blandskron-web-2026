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


class BlogFlowIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="integration-author")
        cls.security = Tag.objects.create(name="Seguridad")
        cls.devops = Tag.objects.create(name="DevOps")

        cls.security_post = Post.objects.create(
            title="Seguridad ficticia para equipos",
            author=cls.author,
            content="Contenido ficticio sobre controles de seguridad.",
        )
        cls.security_post.tags.add(cls.security)

        cls.devops_post = Post.objects.create(
            title="Pipelines ficticios con DevOps",
            author=cls.author,
            content="Contenido ficticio sobre automatización y pipelines.",
        )
        cls.devops_post.tags.add(cls.devops)

    def test_blog_list_reads_posts_from_database_and_renders_template(self):
        response = self.client.get(reverse("blog:blog_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/list.html")
        self.assertContains(response, self.security_post.title)
        self.assertContains(response, self.devops_post.title)

    def test_blog_search_and_tag_filters_cross_view_and_orm(self):
        search_response = self.client.get(
            reverse("blog:blog_list"),
            {"q": "pipelines"},
        )
        tag_response = self.client.get(
            reverse("blog:blog_list"),
            {"tag": self.security.slug},
        )

        self.assertContains(search_response, self.devops_post.title)
        self.assertNotContains(search_response, self.security_post.title)
        self.assertContains(tag_response, self.security_post.title)
        self.assertNotContains(tag_response, self.devops_post.title)

    def test_post_detail_resolves_slug_and_renders_content(self):
        response = self.client.get(
            reverse(
                "blog:post_detail",
                kwargs={"slug": self.security_post.slug},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/detail.html")
        self.assertContains(response, self.security_post.title)
        self.assertContains(response, self.security_post.content)

    def test_unknown_post_is_handled_by_django_404(self):
        response = self.client.get(
            reverse("blog:post_detail", kwargs={"slug": "missing-integration-post"})
        )

        self.assertEqual(response.status_code, 404)
