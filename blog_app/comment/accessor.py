from blog_app.models import Comment
from blog_app.author.accessor import AuthorAccess
from blog_app.category.accessor import CategoryAccess
from blog_app.post.accessor import PostAccess



class CommentAccess:
    
    @staticmethod
    def get_all_comments():
        return Comment.objects.all()
    
    @staticmethod
    def get_comment_by_id(id):
        return Comment.objects.filter(id = id).first()
    
    @staticmethod
    def create_comment(post_id, name, email, content, is_approved = ""):
        post = PostAccess.get_post_by_id(post_id)
        Comment.objects.create(post = post, name = name, email = email, content = content, is_approved = is_approved)

    @staticmethod
    def delete_comment(id):
        comment = CommentAccess.get_comment_by_id(id)
        comment.delete()

    @staticmethod
    def get_comment_by_post(self, post_id):
        post = PostAccess.get_post_by_id(post_id)
        return Comment.objects.filter(post = post).all()