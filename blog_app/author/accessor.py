from blog_app.models import Author

class AuthorAccess:


    @staticmethod
    def get_all_author():
        return Author.objects.filter(active = True).all()

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
