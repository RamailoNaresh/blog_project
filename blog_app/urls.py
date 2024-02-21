from django.urls import path
from blog_app.author import views as author_views
from blog_app.comment import views as comment_views
from blog_app.category import views as category_views
from blog_app.post import views as post_views


urlpatterns = [
    path("v1/authors/", author_views.get_all_author, name = "authors"),
    path("v1/author/<str:id>/", author_views.get_author_by_id, name = 'author-detail'),
    path("v1/create_author/", author_views.create_author, name = "create-author"),
    path("v1/delete_author/<str:id>/", author_views.delete_author, name = "delete-author"),
    path("v1/categories/", category_views.get_all_category, name = "categories"),
    path("v1/category/<str:id>/", category_views.get_category_by_id, name = 'category-detail'),
    path("v1/create_category/", category_views.create_category, name = "create-category"),
    path("v1/delete_category/<str:id>/", category_views.delete_category, name = "delete-category")
]
