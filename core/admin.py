from django.contrib import admin
from .models import PostImages, PostComment, Post

# Register your models here.


class ImagePostAdmin(admin.TabularInline):
    model = PostImages


class CommentAdmin(admin.TabularInline):
    model = PostComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [ImagePostAdmin, CommentAdmin]
