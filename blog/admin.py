from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('author', 'created_date', 'published_date')

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_date')
    search_fields = ('author', 'content')
