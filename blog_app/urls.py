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
    path("v1/update_author/<str:id>/", author_views.update_author, name = "update=author"),
    path("v1/categories/", category_views.get_all_category, name = "categories"),
    path("v1/category/<str:id>/", category_views.get_category_by_id, name = 'category-detail'),
    path("v1/create_category/", category_views.create_category, name = "create-category"),
    path("v1/delete_category/<str:id>/", category_views.delete_category, name = "delete-category"),
    path("v1/update_category/<str:id>/", category_views.update_category, name = "update-category"),
    path("v1/posts/", post_views.get_all_post, name = "posts"),
    path("v1/unpublished_posts/", post_views.get_unpublished_post, name = "unpublished-post"),
    path("v1/post_by_id/<str:id>/", post_views.get_post_by_id, name = "post-by-id"),
    path("v1/post_by_author/<str:id>/", post_views.get_post_by_author, name = "post-by-author"),
    path("v1/post_by_category/<str:id>/", post_views.get_post_by_category, name = "post-by-category"),
    path("v1/post_by_slug/<str:slug>/", post_views.get_post_by_slug, name = "post-by-slug"),
    path("v1/delete_post/<str:id>/", post_views.delete_post, name = "delete-post"),
    path("v1/create_post/", post_views.create_post, name = "create-post"),
    path("v1/update_post/<str:id>/", post_views.update_post, name = "update-post"),
    path("v1/comments/", comment_views.get_all_comments, name = "comments"),
    path("v1/comment_by_id/<str:id>/", comment_views.get_comment_by_id, name = "comment-by-id"),
    path("v1/comment_by_post/<str:post_id>/", comment_views.get_comment_by_post, name = "comment-by-post"),
    path("v1/create_comment/", comment_views.create_comment, name = "create-comment"),
    path("v1/delete_comment/<str:id>/", comment_views.delete_comment, name = "delete-comment"),
    path("v1/update_comment/<str:id>/", comment_views.update_comment, name = "update-comment"),
    path("v1/unapproved_comments/", comment_views.get_unapproved_comments, name = "unapproved-comments"),
]
