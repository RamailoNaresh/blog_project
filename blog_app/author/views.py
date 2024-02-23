from rest_framework.response import Response
from blog_app.author.serializers import AuthorSerializer
from rest_framework.decorators import api_view
from blog_app.author.author import Author
from rest_framework.parsers import JSONParser
from rest_framework import status
from blog_app.util.password_encoder import validate_password
from blog_app.api.response_builder import ResponseBuilder
from blog_app.api import api


@api_view(["GET"])
def get_all_author(request):
    data = Author.get_all_author()
    serializer = AuthorSerializer(data, many = True)
    response_builder = ResponseBuilder()
    return response_builder.get_200_success_response("Data fetched", serializer.data)


@api_view(["GET"])
def get_author_by_id(request, id):
    respones_builder = ResponseBuilder()
    try:
        data = Author.get_author_by_id(id)
        serializer = AuthorSerializer(data)
        return respones_builder.get_200_success_response("Data fetched", serializer.data)
    except Exception as e:
        return respones_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND,str(e))


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
    
@api_view(["PUT", "PATCH"])
def update_author(request, id):
    respones_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        obj = Author.get_author_by_id(id)
        serializer = AuthorSerializer(obj,data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return respones_builder.get_200_success_response("Successfully Updated", serializer.data)
        return respones_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except Exception as e:
        return respones_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND, str(e))



@api_view(["DELETE"])
def delete_author(request, id):
    respones_builder = ResponseBuilder()
    try:
        Author.delete_author(id)
        return respones_builder.get_200_success_response("Data Successfully deleted")
    except Exception as e:
        return respones_builder.get_404_not_found_response(api.AUTHOR_NOT_FOUND)
    
