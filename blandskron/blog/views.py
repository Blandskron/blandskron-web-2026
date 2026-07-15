"""
Blandskron — Open Project

Este código forma parte de un proyecto abierto de uso profesional y educativo.
Puede ser utilizado, modificado y distribuido libremente.

Si utilizas este código en proyectos públicos o comerciales,
se agradece mantener los créditos originales.

https://blandskron.com
"""

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Post, Tag

def blog_list(request):
    posts = Post.objects.all()
    query = request.GET.get("q")
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    
    tag_slug = request.GET.get("tag")
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
        
    return render(request, 'blog/list.html', {
        'posts': posts,
        'tags': Tag.objects.all(),
        'page_title': 'Blog | Blandskron',
        'page_description': 'Artículos de Blandskron sobre tecnología, innovación, desarrollo y ciberseguridad.',
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/detail.html', {
        'post': post,
        'page_title': f'{post.title} | Blog Blandskron',
        'page_description': post.content[:160],
    })
