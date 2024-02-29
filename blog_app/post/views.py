from rest_framework.response import Response
from blog_app.services.tokens import get_logged_user

from blog_app.shared.pagination import paginate
from .serializers import PostSerializer
from .post import Post
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from blog_app.api import api
from blog_app.api.response_builder import ResponseBuilder


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = get_logged_user(request.user.id)
    response_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        data["author"] = user.id
        new_data = Post.create_post(data)
        serializer = PostSerializer(data = new_data)
        if serializer.is_valid():
            serializer.save()
            return response_builder.get_201_success_response("Post successfully created", serializer.data)
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except ValueError as e:
        return response_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_post(request):
    response_builder = ResponseBuilder()
    data = Post.get_all_post()
    posts, page_info = paginate(data, request)
    serializer = PostSerializer(posts, many = True)
    return response_builder.get_200_success_response("Data successfully fetched",page_info, serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_post_by_id(request, id):
    response_builder = ResponseBuilder()
    try:
        data = Post.get_post_by_id(id)
        serializer = PostSerializer(data)
        return response_builder.get_201_success_response("Data successfully fetched", serializer.data)
    except ValueError as e:
        return response_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_post_by_slug(request, slug):
    response_builder = ResponseBuilder()
    try:
        data = Post.get_post_by_slug(slug)
        serializer = PostSerializer(data)
        return response_builder.get_201_success_response("Data successfully fetched", serializer.data)
    except ValueError as e:
        return response_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_post_by_author(request, id):
    response_builder = ResponseBuilder()
    try:
        data = Post.get_post_by_author(id)
        posts, page_info = paginate(data, request)
        serializer = PostSerializer(posts, many = True)
        return response_builder.get_200_success_response("Data successfully fetched",page_info, serializer.data)
    except ValueError as e:
        return response_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_post_by_category(request, id):
    response_builder = ResponseBuilder()
    try:
        data = Post.get_post_by_category(id)
        posts, page_info = paginate(data, request)
        serializer = PostSerializer(posts, many = True)
        return response_builder.get_200_success_response("Data successfully fetched",page_info, serializer.data)
    except ValueError as e:
        return response_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_post(request, id):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id) 
        post = Post.get_post_by_id(id)
        if user.role == "Admin" or user.id == post.author:
            Post.delete_post(id)
            return response_builder.get_201_success_response("Data successfully deleted")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        return response_builder.get_404_not_found_response(api.POST_NOT_FOUND)
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_post(request, id):
    response_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        post = Post.get_post_by_id(id)
        user = get_logged_user(request.user.id) 
        if user.role == "Admin" or user.id == post.author.id:
            serializer = PostSerializer(post, data = data, partial  = True)
            if serializer.is_valid():
                serializer.save()
                return response_builder.get_201_success_response("Data successfully updated", serializer.data)
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        return response_builder.get_404_not_found_response(api.POST_NOT_FOUND)
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_unpublished_post(request):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin":
            data = Post.get_unpublished_post()
            posts, page_info = paginate(data, request)
            serializer = PostSerializer(posts, many = True)
            return response_builder.get_200_success_response("Data successfully fetched",page_info, serializer.data)
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        return response_builder.get_400_bad_request_response(api.POST_NOT_FOUND, str(e))
    except Exception as e:
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    
