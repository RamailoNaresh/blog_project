from blog_app.models import Post
from blog_app.author.accessor import AuthorAccess
from blog_app.category.accessor import CategoryAccess

class PostAccess:

    @staticmethod
    def get_all_post():
        return Post.objects.filter(is_active = True, is_published = True).order_by("-created_at").all()
    
    @staticmethod
    def get_post_by_id(id):
        return Post.objects.filter(id = id, is_active = True, is_published = True).first()
    
    @staticmethod
    def get_post_by_author(id):
        author = AuthorAccess.get_author_by_id(id)
        return Post.objects.filter(author = author, is_active = True).all()
    
    @staticmethod
    def get_post_by_category(id):
        category = CategoryAccess.get_category_by_id(id)
        post = Post.objects.filter(categories__id = id, is_active = True, is_published = True).all()
        return post
    
    @staticmethod
    def get_post_by_slug(slug):
        return Post.objects.filter(slug = slug, is_active = True, is_published = True).first()
    


    @staticmethod
    def create_post(author_id, title, slug, content,cat_id, is_published = "", published_at = ""):
        author = AuthorAccess.get_author_by_id(author_id)
        category = CategoryAccess.get_category_by_id(cat_id)
        Post.objects.create(title = title, slug = slug, author = author, content = content, published_at = published_at, categories = category, is_published = is_published)
        
    @staticmethod
    def delete_post(id):
        post = PostAccess.get_post_by_id(id)
        post.delete()

    @staticmethod
    def get_unpublished_post():
        return Post.objects.filter(is_published = False).all()


