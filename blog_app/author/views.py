from rest_framework.response import Response
from blog_app.author.serializers import AuthorSerializer
from rest_framework.decorators import api_view
from blog_app.author.author import AuthorService
from rest_framework.parsers import JSONParser

@api_view(["GET"])
def get_all_author(request):
    data = AuthorService.get_all_author()
    serializer = AuthorSerializer(data, many = True)
    return Response(serializer.data)


@api_view(["GET"])
def get_author_by_id(request, id):
    try:
        data = AuthorService.get_author_by_id(id)
        serializer = AuthorSerializer(data)
        return Response(serializer.data)
    except Exception as e:
        return Response(str(e))


@api_view(["POST"])
def create_author(request):
    try:
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data =data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "data successfully created", "data": data})
        return Response({"error": serializer.errors})
    except Exception as e:
        return Response({"error": str(e)})
    
@api_view(["DELETE"])
def delete_author(request, id):
    try:
        AuthorService.delete_author(id)
        return Response({"message": "Data successfully deleted"})
    except Exception as e:
        return Response({"error": str(e)})

