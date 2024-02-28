from blog_app.models import ForgetPassword



class ForgetPasswordAccess:

    @staticmethod
    def get_forget_password_by_token(token):
        return ForgetPassword.objects.filter(token = token).first()
    
    @staticmethod
    def get_forget_password_by_author(author):
        return ForgetPassword.objects.filter(author = author).first()


    @staticmethod
    def delete_forget_password(author):
        obj = ForgetPassword.objects.filter(author = author).first()
        obj.delete()