from blog_app.models import Post
from author.accessor import AuthorAccess
from category.accessor import CategoryAccess

class PostAccess:

    @staticmethod
    def get_all_post():
        return Post.objects.all()
    
    @staticmethod
    def get_post_by_id(id):
        return Post.objects.filter(id = id).first()
    
    @staticmethod
    def get_post_by_author(id):
        author = AuthorAccess.get_author_by_id(id)
        return Post.objects.filter(author = author).all()
    
    @staticmethod
    def get_post_by_category(id):
        category = CategoryAccess.get_category_by_id(id)
        return Post.objects.filter(category = category).all()
    
    @staticmethod
    def create_post(author_id, title, slug, content,cat_id, is_published = "", published_at = ""):
        author = AuthorAccess.get_author_by_id(author_id)
        category = CategoryAccess.get_category_by_id(cat_id)
        Post.objects.create(title = title, slug = slug, author = author, content = content, published_at = published_at, categories = category, is_published = is_published)
        
    @staticmethod
    def delete_post(id):
        post = PostAccess.get_post_by_id(id)
        post.delete()


