from blog_app.api import api
from blog_app.api.response_builder import ResponseBuilder
from blog_app.author.author import Author
from rest_framework.decorators import api_view
from blog_app.services.email_service import send_forget_password_link
from .forgetpassword import ForgetPassword
from .serializers import ForgetPasswordSerializer, ChangePasswordSerializer
from .accessor import ForgetPasswordAccess
from rest_framework.parsers import JSONParser


@api_view(["POST"])
def forget_password(request):
    response_builder = ResponseBuilder()
    try:
        email = request.data.get("email")
        if email is None:
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Email is required")
        author = Author.get_user_by_email(email)
        check_token = ForgetPasswordAccess.get_forget_password_by_author(author.id)
        if check_token:
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Email already send")
        token_data = send_forget_password_link(author)
        if token_data == True:
            return response_builder.get_201_success_response("Please check your email.")
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, token_data)
    except ValueError as e:
        return response_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND,str(e))
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    


@api_view(["POST"])
def check_forget_password(request, token):
    response_builder = ResponseBuilder()
    try:
        password = request.data["password"]
        if password == "":
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Password field is required")
        forget_password = ForgetPassword.get_forget_password_by_token(token)
        author = forget_password.author
        author.password = password
        author.save()
        ForgetPassword.delete_forget_password(author.id)
        return response_builder.get_201_success_response("Password successfully changed")
    except KeyError:
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "All fields is required")
    except ValueError as e:
        return response_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND,str(e))
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))