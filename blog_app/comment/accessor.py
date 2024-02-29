from blog_app.models import Comment
from blog_app.author.accessor import AuthorAccess
from blog_app.category.accessor import CategoryAccess
from blog_app.post.accessor import PostAccess



class CommentAccess:
    
    @staticmethod
    def get_all_comments():
        return Comment.objects.filter(is_approved = True).all()
    
    @staticmethod
    def get_comment_by_id(id):
        return Comment.objects.filter(id = id).first()
    
    @staticmethod
    def create_comment(post_id, author_id, content, is_approved = ""):
        post = PostAccess.get_post_by_id(post_id)
        author = AuthorAccess.get_author_by_id(author_id)
        Comment.objects.create(post = post, author = author, content = content, is_approved = is_approved)

    @staticmethod
    def delete_comment(id):
        comment = CommentAccess.get_comment_by_id(id)
        comment.delete()

    @staticmethod
    def get_comment_by_post(post_id):
        post = PostAccess.get_post_by_id(post_id)
        return Comment.objects.filter(post = post, is_approved = True).all()
    
    @staticmethod
    def get_comment_by_author(author_id):
        author = AuthorAccess.get_author_by_id(author_id)
        return Comment.objects.filter(author = author, is_approved = True).all()
    

    @staticmethod
    def get_unapproved_comments():
        return Comment.objects.filter(is_approved = False).all()
    
    @staticmethod
    def approve_comment(id):
        data  = CommentAccess.get_comment_by_id(id)
        data.is_approved = True
        data.save()