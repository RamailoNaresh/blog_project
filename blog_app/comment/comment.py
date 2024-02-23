from .accessor import CommentAccess
from blog_app.post.post import Post


class Comment:

    @staticmethod
    def get_all_comments():
        data = CommentAccess.get_all_comments()
        if data:
            return data
        raise Exception("No data available")
    

    @staticmethod
    def get_comment_by_id(id):
        data =CommentAccess.get_comment_by_id(id)
        if data:
            return data
        raise Exception("Data doesn't exists")
    
    @staticmethod
    def get_comment_by_post(post_id):
        post = Post.get_post_by_id(post_id)
        data = CommentAccess.get_comment_by_post(post_id)
        if data:
            return data
        raise Exception("No comments available")
    
    @staticmethod
    def delete_comment(id):
        comment = CommentAccess.get_comment_by_id(id)
        if not comment:
            raise Exception("Comment doesn't exists")
        CommentAccess.delete_comment(id)

    @staticmethod
    def get_unapproved_comments():
        data = CommentAccess.get_unapproved_comments()
        if not data:
            raise Exception("No unapproved data")
        return data
    
    @staticmethod
    def approve_comment(id):
        data = CommentAccess.get_comment_by_id(id)
        if data:
            if data.is_approved:
                raise Exception("Comment is already verified")
            CommentAccess.approve_comment(id)
            return data
        raise Exception("Data doesn't exists")
