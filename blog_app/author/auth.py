from blog_app.author.author import Author
from rest_framework.decorators import api_view
from rest_framework.views import csrf_exempt
from blog_app.api.response_builder import ResponseBuilder
from blog_app.api import api
from blog_app.author.serializers import AuthorSerializer
from rest_framework.parsers import JSONParser
from blog_app.services.email_service import send_otp_mail
from django.utils import timezone
from django.utils.timezone import timedelta

@api_view(["POST"])
@csrf_exempt
def login_user(request):
    response_builder = ResponseBuilder()
    try:
        email = request.data.get("email")
        password = request.data.get("password")
        if email == "" or password == "":
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Fields cannot be empty")
        user, token = Author.login_user(email, password)
        author = AuthorSerializer(user)
        data = {
            "user": author.data,
            "token": token
        }
        return response_builder.get_200_login_success_response(api.LOGIN_SUCCESS, data)
    except ValueError as e:
        return response_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND,str(e))
    except:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    


@api_view(["POST"])
@csrf_exempt
def create_author(request):
    response_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data =data)
        if serializer.is_valid():
            serializer.save()
            author = Author.get_user_by_email(serializer.data["email"])
            send_otp_mail(author)
            return response_builder.get_201_success_response("Data succesfully created. Please check you email", serializer.data)
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    

@api_view(["POST"])
@csrf_exempt
def check_otp(request):
    response_builder = ResponseBuilder()
    try:
        otp = request.data.get("otp")
        email = request.data.get("email")
        if otp is None or email is None:
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "All Fields are required")
        author = Author.get_user_by_email(email)
        if author.is_verified:
            return response_builder.get_201_success_response("User is already verified")
        if author.otp != otp:
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Invalid OTP")
        if author.otp_sent_date + timedelta(minutes=10) <= timezone.now():
            author.otp = None
            author.save()
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Invalid OTP")
        author.otp = None
        author.is_verified = True
        author.save()
        serializer = AuthorSerializer(author)
        return response_builder.get_201_success_response("User successfully verified", serializer.data)
    except ValueError as e:
        return response_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND,str(e))
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    