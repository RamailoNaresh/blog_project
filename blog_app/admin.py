from django.contrib import admin
from .models import Post, Author, Category, Comment, ForgetPassword
from import_export.admin import ImportExportModelAdmin

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id","title", "author")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","author","content", "post")

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ("id","title")

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id","name", "email")
    

@admin.register(ForgetPassword)
class ForgetPasswordAdmin(admin.ModelAdmin):
    list_display = ("token", "author")
