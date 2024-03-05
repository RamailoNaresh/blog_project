from blog_app.author.accessor import AuthorAccess
from blog_app.util.password_encoder import validate_password, encrypt_password
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
        if data:
            return data
        raise ValueError("User doesn't exists")
    
    @staticmethod
    def login_user(email , password):
        user = Author.get_user_by_email(email)
        if not user:
            raise ValueError("Email didnt't matched")
        if not user.is_verified:
            raise ValueError("User is not verified")
        check_password = validate_password(password, user.password)
        if not check_password:
            raise ValueError("Password didn't matched")
        token = generate_token(user)
        return user, token
    
    @staticmethod
    def change_password(author_id, password):
        author = Author.get_author_by_id(author_id)
        AuthorAccess.change_password(author_id,password)


    @staticmethod
    def verify_author(author_id):
        author = Author.get_author_by_id(author_id)
        AuthorAccess.verify_author(author_id)

    @staticmethod
    def delete_otp(author_id):
        author = Author.get_author_by_id(author_id)
        AuthorAccess.delete_otp(author_id)

