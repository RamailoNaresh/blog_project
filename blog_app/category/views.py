from .category import Category
from rest_framework.response import Response
from .serializers import CategorySerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from blog_app.api import api
from blog_app.api.response_builder import ResponseBuilder
from blog_app.shared.pagination import paginate


@api_view(["GET"])
def get_all_category(request):
    response_builder = ResponseBuilder()
    data = Category.get_all_category()
    categories, page_info = paginate(data, request)
    serializer = CategorySerializer(categories, many = True)
    return response_builder.get_200_success_response("Data fetched",page_info, serializer.data)


@api_view(["GET"])
def get_category_by_id(request, id):
    response_builder = ResponseBuilder()
    try:
        data = Category.get_category_by_id(id)
        serializer = CategorySerializer(data)
        return response_builder.get_200_success_response("Data fetched", serializer.data)
    except Exception as e:
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))
        


@api_view(["POST"])
def create_category(request):
    response_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data =data)
        if serializer.is_valid():
            serializer.save()
            return response_builder.get_201_success_response("Category Successfully created", serializer.data)
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except Exception as e:
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))
    
@api_view(["PUT", "PATCH"])
def update_category(request, id):
    response_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        obj = Category.get_category_by_id(id)
        serializer = CategorySerializer(obj,data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return response_builder.get_200_success_response("Category Successfully updated", serializer.data)
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except Exception as e:
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))




@api_view(["DELETE"])
def delete_category(request, id):
    response_builder = ResponseBuilder()
    try:
        Category.delete_category(id)
        return response_builder.get_200_success_response("Category Successfully deleted")
    except Exception as e:
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))