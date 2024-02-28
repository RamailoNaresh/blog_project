from .accessor import ForgetPasswordAccess
from blog_app.author.author import Author

class ForgetPassword:

    @staticmethod
    def get_forget_password_by_token(token):
        data = ForgetPasswordAccess.get_forget_password_by_token(token)
        if data is not None:
            return data
        raise ValueError("Data doesn't exists")
    

    @staticmethod
    def get_forget_password_by_author(author_id):
        author = Author.get_author_by_id(author_id)
        data = ForgetPasswordAccess.get_forget_password_by_author(author)
        if data:
            return data
        raise ValueError("Data doesn't exists")
    

    @staticmethod
    def delete_forget_password(author):
        data = ForgetPassword.get_forget_password_by_author(author)
        ForgetPasswordAccess.delete_forget_password(author)

