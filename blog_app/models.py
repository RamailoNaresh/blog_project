from django.db import models
from blog_app.util.util import get_char_uuid
from blog_app.util.password_encoder import encrypt_password, validate_password


class BaseModel(models.Model):
    id = models.CharField(primary_key = True, default = get_char_uuid, max_length = 100, db_index= True, editable = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Author(BaseModel):
    ADMIN = "Admin"
    USER = "User"
    CHOICES = (
        (ADMIN, "Admin"),
        (USER, "USER"),
    )
    
    name = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    bio = models.TextField(blank = True)
    active = models.BooleanField(default = True)
    role = models.CharField(max_length = 50, choices = CHOICES)
    password = models.CharField(max_length = 255)
    otp = models.CharField(max_length = 10, null = True, blank = True)
    otp_sent_date = models.DateTimeField(null = True, blank = True)
    is_verified = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        author = Author.objects.filter(id = self.pk).first()
        if author:
            checking_pass = validate_password(self.password, author.password)
            if not checking_pass:
                self.password = encrypt_password(self.password)
        else:
            self.password = encrypt_password(self.password)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    

class Category(BaseModel):

    TECHNOLOGY = "Technology"
    MOVIES = "Movies"
    ENTERTAINMENT = "Entertainment"
    EDUCATION = "Education"
    SPORTS = "Sports"
    TRAVEL = "Travel"
    COUNTRY = "Country"
    CULTURE = "Culture"
    OTHER = "Other"

    CHOICES = (
        (TECHNOLOGY, "Information and Technology"),
        (MOVIES, "Movies"),
        (COUNTRY, "Countries"),
        (CULTURE, "Cultural"),
        (ENTERTAINMENT, "Entertainment and videos"),
        (EDUCATION, "Education and Learning"),
        (SPORTS, "Sports and Fitness"),
        (TRAVEL, "Travel and Adventure"),
        (OTHER, "Other"),
    )
    title = models.CharField(max_length=150, unique=True, choices=CHOICES)
    description = models.TextField(blank=True)

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
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    content = models.TextField()
    is_approved = models.BooleanField(default = False)

    def __str__(self):
        return "Comment by {self.name} on {self.post.title}"
    

class ForgetPassword(BaseModel):
    token = models.CharField(max_length = 255)
    author = models.OneToOneField(Author, on_delete = models.CASCADE)

