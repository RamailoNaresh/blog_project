from django.db.models import Q
from blog_app.models import Author

class AuthorAccess:


    @staticmethod
    def get_all_author():
        return Author.objects.filter(active = True).all().order_by("-created_at")

    @staticmethod
    def get_author_by_id(id):
        return Author.objects.filter(id = id, active = True).first()

    @staticmethod
    def create_author(name, email, bio = ""):
        Author.objects.create(name = name, email  = email, bio = bio)

    @staticmethod
    def delete_author(id):
        author = AuthorAccess.get_author_by_id(id)
        author.active = False
        author.save()

    @staticmethod
    def get_user_by_email(email):
        return Author.objects.filter(email__iexact = email, active = True).first()
    
    @staticmethod
    def change_password(author_id, password):
        author = AuthorAccess.get_author_by_id(author_id)
        author.password = password
        author.save()

    @staticmethod
    def verify_author(author_id):
        author = AuthorAccess.get_author_by_id(author_id)
        author.is_verified = True
        author.otp = None
        author.save()


    @staticmethod
    def delete_otp(author_id):
        author = AuthorAccess.get_author_by_id(author_id)
        author.otp = None
        author.save()

    @staticmethod
    def get_author_by_email_or_name(input_data):
        data = Author.objects.filter(Q(name__icontains = input_data) | Q(email__icontains = input_data)).values()
        return data