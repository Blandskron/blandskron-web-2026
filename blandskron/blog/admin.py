from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Post, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'content')
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 25, 
                'style': 'width: 100%; font-family: "Fira Code", monospace; background: #1e1e1e; color: #d4d4d4; padding: 15px;'
            })
        },
    }