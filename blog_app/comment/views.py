from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .comment import Comment
from rest_framework.decorators import api_view
from .serializers import CommentSerializer
from rest_framework import status

@api_view(["GET"])
def get_all_comments(request):
    try:
        data = Comment.get_all_comments()
        serializer = CommentSerializer(data, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def get_comment_by_id(request, id):
    try:
        data = Comment.get_comment_by_id(id)
        serializer = CommentSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def get_comment_by_post(request, post_id):
    try:
        data = Comment.get_comment_by_post(post_id)
        serializer = CommentSerializer(data, many = True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
def create_comment(request):
    try:
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Comment successfully added", "Data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["DELETE"])
def delete_comment(request, id):
    try:
        Comment.delete_comment(id)
        return Response({"Message" : "Data successfully deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["PUT", "PATCH"])
def update_comment(request, id):
    try:
        data = JSONParser().parse(request)
        comment = Comment.get_comment_by_id(id)
        serializer = CommentSerializer(comment, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Successfully updated", "Data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def get_unapproved_comments(request):
    try:
        data = Comment.get_unapproved_comments()
        serializer = CommentSerializer(data, many  = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error", str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def approve_comment(request, id):
    try:
        data = Comment.approve_comment(id)
        serializer = CommentSerializer(data)
        return Response({"Mssage": "Comment is approved"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)