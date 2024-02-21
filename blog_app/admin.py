from django.contrib import admin
from .models import Post, Author, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id","title", "author")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","name", "email", "post")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","title")

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id","name", "email")
    


