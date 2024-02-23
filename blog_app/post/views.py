from rest_framework.response import Response
from .serializers import PostSerializer
from .post import Post
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status


@api_view(["POST"])
def create_post(request):
    try:
        data = JSONParser().parse(request)
        new_data = Post.create_post(data)
        serializer = PostSerializer(data = new_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Data successfully created", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_post(request):
    data = Post.get_all_post()
    serializer = PostSerializer(data, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_post_by_id(request, id):
    try:
        data = Post.get_post_by_id(id)
        serializer = PostSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def get_post_by_slug(request, slug):
    try:
        data = Post.get_post_by_slug(slug)
        serializer = PostSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_post_by_author(request, id):
    try:
        data = Post.get_post_by_author(id)
        serializer = PostSerializer(data, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def get_post_by_category(request, id):
    try:
        data = Post.get_post_by_category(id)
        serializer = PostSerializer(data, many  =True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["DELETE"])
def delete_post(request, id):
    try: 
        Post.delete_post(id)
        return Response({"Message": "Data successfully delete"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["PUT", "PATCH"])
def update_post(request, id):
    try:
        data = JSONParser().parse(request)
        post = Post.get_post_by_id(id)
        serializer = PostSerializer(post, data = data, partial  = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Data successfully updated", "Data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def get_unpublished_post(request):
    try:
        data = Post.get_unpublished_post()
        serializer = PostSerializer(data, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
