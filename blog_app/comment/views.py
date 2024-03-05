from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from blog_app.shared.pagination import paginate
from .comment import Comment
from rest_framework.decorators import api_view
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from blog_app.services.tokens import get_logged_user
from blog_app.api import api
from blog_app.api.response_builder import ResponseBuilder
from blog_app.services.logger import logger_info, logger_warning


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_comments(request):
    response_builder = ResponseBuilder()
    try:
        data = Comment.get_all_comments()
        comments, page_info = paginate(data, request)
        serializer = CommentSerializer(comments, many = True)
        return response_builder.get_200_success_response("Data fetched",page_info, serializer.data)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_404_not_found_response(api.COMMENT_NOT_FOUND)
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_comment_by_id(request, id):
    response_builder = ResponseBuilder()
    user = get_logged_user(request.user.id)
    try:
        data = Comment.get_comment_by_id(id)
        serializer = CommentSerializer(data)
        return response_builder.get_201_success_response("Data fetched", serializer.data)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_404_not_found_response(api.COMMENT_NOT_FOUND)
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_comment_by_post(request, post_id):
    response_builder = ResponseBuilder()
    try:
        data = Comment.get_comment_by_post(post_id)
        comments, page_info = paginate(data, request)
        serializer = CommentSerializer(comments, many = True)
        return response_builder.get_200_success_response("Data fetched",page_info, serializer.data)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_404_not_found_response(api.COMMENT_NOT_FOUND)
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request):
    response_builder = ResponseBuilder()
    user = get_logged_user(request.user.id)
    try:
        data = JSONParser().parse(request)
        data["author"] = user.id
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            logger_info.info(f"{user.email} added comment")
            return response_builder.get_201_success_response("Comment successfully added", serializer.data)
        logger_warning.warning(serializer.errors)
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_400_bad_request_response(api.COMMENT_NOT_FOUND, str(e))
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, id):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        comment = Comment.get_comment_by_id(id)
        if user.role == "Admin" or comment.author == user.id:
            Comment.delete_comment(id)
            logger_info.info(f"{user.email} deleted comment")
            return response_builder.get_201_success_response("Data succesfully deleted")
        logger_warning.warning(f"Access denied {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_404_not_found_response(api.COMMENT_NOT_FOUND)
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_comment(request, id):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        comment = Comment.get_comment_by_id(id)
        if user.role == "Admin" or comment.author == user.id:
            data = JSONParser().parse(request)
            serializer = CommentSerializer(comment, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                logger_info.info(f"{user.email} updated comment")
                return response_builder.get_201_success_response("Comment successfully updated", serializer.data)
            logger_warning.warning(serializer.errors)
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
        logger_warning.warning(f"Access denied {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_400_bad_request_response(api.COMMENT_NOT_FOUND, str(e))
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_unapproved_comments(request):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin":
            data = Comment.get_unapproved_comments()
            comments, page_info = paginate(data, request)
            serializer = CommentSerializer(comments, many = True)
            return response_builder.get_200_success_response("Data fetched",page_info, serializer.data)
        logger_warning.warning(f"Access denied {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_404_not_found_response(api.COMMENT_NOT_FOUND)
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def approve_comment(request, id):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin":
            data = Comment.approve_comment(id)
            serializer = CommentSerializer(data)
            logger_info.info(f"{user.email} approved comment")
            return response_builder.get_201_success_response("Data fetched", serializer.data)
        logger_warning.warning(f"Access denied {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_400_bad_request_response(api.COMMENT_NOT_FOUND, str(e))
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))