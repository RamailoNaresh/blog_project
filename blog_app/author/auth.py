from blog_app.author.author import Author
from rest_framework.decorators import api_view
from rest_framework.views import csrf_exempt
from blog_app.api.response_builder import ResponseBuilder
from blog_app.api import api
from blog_app.author.serializers import AuthorSerializer
from rest_framework.parsers import JSONParser



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
    except Exception as e:
        return response_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND, str(e))
    


@api_view(["POST"])
def create_author(request):
    respones_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data =data)
        if serializer.is_valid():
            serializer.save()
            return respones_builder.get_201_success_response("Data succesfully created", serializer.data)
        return respones_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except Exception as e:
        return respones_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND, str(e))
    