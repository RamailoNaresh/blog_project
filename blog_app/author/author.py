from .accessor import AuthorAccess
from blog_app.util.password_encoder import validate_password
from blog_app.services.tokens import generate_token


class Author:

    @staticmethod
    def get_all_author():
        data = AuthorAccess.get_all_author()
        return data
    
    @staticmethod
    def get_author_by_id(id):
        data = AuthorAccess.get_author_by_id(id)
        if data:
            return data
        raise ValueError("Data not found")
    
    @staticmethod
    def delete_author(id):
        data = AuthorAccess.get_author_by_id(id)
        if data is None:
            raise ValueError("Data not found")
        AuthorAccess.delete_author(id)

    @staticmethod
    def get_user_by_email(email):
        data = AuthorAccess.get_user_by_email(email)
        if email:
            return data
        raise ValueError("User doesn't exists")
    
    @staticmethod
    def login_user(email , password):
        user = Author.get_user_by_email(email)
        if not user:
            raise ValueError("Email or password didnt't matched")
        check_password = validate_password(password, user.password)
        if not check_password:
            raise ValueError("Email or password didn't matched")
        token = generate_token(user)
        return user, token