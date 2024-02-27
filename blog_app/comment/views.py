from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from blog_app.shared.pagination import paginate
from .comment import Comment
from rest_framework.decorators import api_view
from .serializers import CommentSerializer
from rest_framework import status
from blog_app.api import api
from blog_app.api.response_builder import ResponseBuilder

@api_view(["GET"])
def get_all_comments(request):
    response_builder = ResponseBuilder()
    try:
        data = Comment.get_all_comments()
        comments, page_info = paginate(data, request)
        serializer = CommentSerializer(comments, many = True)
        return response_builder.get_200_success_response("Data fetched",page_info, serializer.data)
    except Exception as e:
        return response_builder.get_404_not_found_response(api.COMMENT_NOT_FOUND)
    

@api_view(["GET"])
def get_comment_by_id(request, id):
    response_builder = ResponseBuilder()
    try:
        data = Comment.get_comment_by_id(id)
        serializer = CommentSerializer(data)
        return response_builder.get_200_success_response("Data fetched", serializer.data)
    except Exception as e:
        return response_builder.get_404_not_found_response(api.COMMENT_NOT_FOUND)
    

@api_view(["GET"])
def get_comment_by_post(request, post_id):
    response_builder = ResponseBuilder()
    try:
        data = Comment.get_comment_by_post(post_id)
        comments, page_info = paginate(data, request)
        serializer = CommentSerializer(comments, many = True)
        return response_builder.get_200_success_response("Data fetched",page_info, serializer.data)
    except Exception as e:
        return response_builder.get_404_not_found_response(api.COMMENT_NOT_FOUND)
    

@api_view(["POST"])
def create_comment(request):
    response_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return response_builder.get_201_success_response("Comment successfully added", serializer.data)
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except Exception as e:
        return response_builder.get_400_bad_request_response(api.COMMENT_NOT_FOUND, str(e))
    


@api_view(["DELETE"])
def delete_comment(request, id):
    response_builder = ResponseBuilder()
    try:
        Comment.delete_comment(id)
        return response_builder.get_200_success_response("Data succesfully deleted")
    except Exception as e:
        return response_builder.get_404_not_found_response(api.COMMENT_NOT_FOUND)
    
@api_view(["PUT", "PATCH"])
def update_comment(request, id):
    response_builder = ResponseBuilder()
    try:
        data = JSONParser().parse(request)
        comment = Comment.get_comment_by_id(id)
        serializer = CommentSerializer(comment, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return response_builder.get_200_success_response("Comment successfully updated", serializer.data)
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    except Exception as e:
        return response_builder.get_400_bad_request_response(api.COMMENT_NOT_FOUND, str(e))
    
@api_view(["GET"])
def get_unapproved_comments(request):
    response_builder = ResponseBuilder()
    try:
        data = Comment.get_unapproved_comments()
        comments, page_info = paginate(data, request)
        serializer = CommentSerializer(comments, many = True)
        return response_builder.get_200_success_response("Data fetched",page_info, serializer.data)
    except Exception as e:
        return response_builder.get_404_not_found_response(api.COMMENT_NOT_FOUND)
    

@api_view(["GET"])
def approve_comment(request, id):
    response_builder = ResponseBuilder()
    try:
        data = Comment.approve_comment(id)
        serializer = CommentSerializer(data)
        return response_builder.get_200_success_response("Data fetched", serializer.data)
    except Exception as e:
        return response_builder.get_400_bad_request_response(api.COMMENT_NOT_FOUND, str(e))