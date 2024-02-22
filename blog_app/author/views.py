from rest_framework.response import Response
from blog_app.author.serializers import AuthorSerializer
from rest_framework.decorators import api_view
from blog_app.author.author import AuthorService
from rest_framework.parsers import JSONParser
from rest_framework import status


@api_view(["GET"])
def get_all_author(request):
    data = AuthorService.get_all_author()
    serializer = AuthorSerializer(data, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_author_by_id(request, id):
    try:
        data = AuthorService.get_author_by_id(id)
        serializer = AuthorSerializer(data)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def create_author(request):
    try:
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data =data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "data successfully created", "data": data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["PUT", "PATCH"])
def update_author(request, id):
    try:
        data = JSONParser().parse(request)
        obj = AuthorService.get_author_by_id(id)
        serializer = AuthorSerializer(obj,data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def delete_author(request, id):
    try:
        AuthorService.delete_author(id)
        return Response({"message": "Data successfully deleted"}, status= status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

