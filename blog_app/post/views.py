from rest_framework.response import Response

from blog_app.shared.pagination import paginate
from .serializers import PostSerializer
from .post import Post
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from blog_app.api import api
from blog_app.api.response_builder import ResponseBuilder


@api_view(["POST"])
def create_post(request):
    respones_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        new_data = Post.create_post(data)
        serializer = PostSerializer(data = new_data)
        if serializer.is_valid():
            serializer.save()
            return respones_builder.get_201_success_response("Post successfully created", serializer.data)
        return respones_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except Exception as e:
        return respones_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))


@api_view(["GET"])
def get_all_post(request):
    respones_builder = ResponseBuilder()
    data = Post.get_all_post()
    posts, page_info = paginate(data, request)
    serializer = PostSerializer(posts, many = True)
    return respones_builder.get_200_success_response("Data successfully fetched",page_info, serializer.data)


@api_view(["GET"])
def get_post_by_id(request, id):
    respones_builder = ResponseBuilder()
    try:
        data = Post.get_post_by_id(id)
        serializer = PostSerializer(data)
        return respones_builder.get_200_success_response("Data successfully fetched", serializer.data)
    except Exception as e:
        return respones_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))
    
@api_view(["GET"])
def get_post_by_slug(request, slug):
    respones_builder = ResponseBuilder()
    try:
        data = Post.get_post_by_slug(slug)
        serializer = PostSerializer(data)
        return respones_builder.get_200_success_response("Data successfully fetched", serializer.data)
    except Exception as e:
        return respones_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))

@api_view(["GET"])
def get_post_by_author(request, id):
    respones_builder = ResponseBuilder()
    try:
        data = Post.get_post_by_author(id)
        posts, page_info = paginate(data, request)
        serializer = PostSerializer(posts, many = True)
        return respones_builder.get_200_success_response("Data successfully fetched",page_info, serializer.data)
    except Exception as e:
        return respones_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))
    
@api_view(["GET"])
def get_post_by_category(request, id):
    respones_builder = ResponseBuilder()
    try:
        data = Post.get_post_by_category(id)
        posts, page_info = paginate(data, request)
        serializer = PostSerializer(posts, many = True)
        return respones_builder.get_200_success_response("Data successfully fetched",page_info, serializer.data)
    except Exception as e:
        return respones_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))
    
@api_view(["DELETE"])
def delete_post(request, id):
    respones_builder = ResponseBuilder()
    try: 
        Post.delete_post(id)
        return respones_builder.get_201_success_response("Data successfully deleted")
    except Exception as e:
        return respones_builder.get_404_not_found_response(api.POST_NOT_FOUND)
    

@api_view(["PUT", "PATCH"])
def update_post(request, id):
    respones_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        post = Post.get_post_by_id(id)
        serializer = PostSerializer(post, data = data, partial  = True)
        if serializer.is_valid():
            serializer.save()
            return respones_builder.get_200_success_response("Data successfully updated", serializer.data)
        return respones_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except Exception as e:
        return respones_builder.get_404_not_found_response(api.POST_NOT_FOUND)
    

@api_view(["GET"])
def get_unpublished_post(request):
    respones_builder = ResponseBuilder()
    try:
        data = Post.get_unpublished_post()
        posts, page_info = paginate(data, request)
        serializer = PostSerializer(posts, many = True)
        return respones_builder.get_200_success_response("Data successfully fetched",page_info, serializer.data)
    except Exception as e:
        return respones_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))
    
