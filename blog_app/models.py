from django.db import models
from blog_app.util.util import get_char_uuid


class BaseModel(models.Model):
    id = models.CharField(primary_key = True, default = get_char_uuid, max_length = 100, db_index= True, editable = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Author(BaseModel):
    name = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    bio = models.TextField(blank = True)
    active = models.BooleanField(default = True)

    def __str__(self):
        return self.name
    

class Category(BaseModel):
    title = models.CharField(max_length = 255, unique = True)
    description = models.TextField(blank = True)

    def __str__(self):
        return self.title
    

class Post(BaseModel):
    title = models.CharField(max_length = 255, unique = True)
    slug = models.SlugField(max_length = 255, unique = True)
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name = "posts")
    content = models.TextField()
    published_at = models.DateTimeField(null = True, blank = True)
    categories = models.ManyToManyField(Category, related_name="posts")
    is_published = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.title
    

class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
    name = models.CharField(max_length = 255)
    email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default = False)

    def __str__(self):
        return "Comment by {self.name} on {self.post.title}"