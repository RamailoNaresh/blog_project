from .category import CategoryService
from rest_framework.response import Response
from .serializers import CategorySerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view


@api_view(["GET"])
def get_all_category(request):
    data = CategoryService.get_all_category()
    serializer = CategorySerializer(data, many = True)
    return Response(serializer.data)


@api_view(["GET"])
def get_category_by_id(request, id):
    try:
        data = CategoryService.get_category_by_id(id)
        serializer = CategorySerializer(data)
        return Response(serializer.data)
    except Exception as e:
        return Response({"Error": str(e)})
        


@api_view(["POST"])
def create_category(request):
    try:
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data =data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "data successfully created", "data": data})
        return Response({"error": serializer.errors})
    except Exception as e:
        return Response({"error": str(e)})
    
@api_view(["PUT", "PATCH"])
def update_category(request, id):
    try:
        data = JSONParser().parse(request)
        obj = CategoryService.get_category_by_id(id)
        serializer = CategorySerializer(obj,data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    except Exception as e:
        return Response({"Error": str(e)})




@api_view(["DELETE"])
def delete_category(request, id):
    try:
        CategoryService.delete_category(id)
        return Response({"message": "Data successfully deleted"})
    except Exception as e:
        return Response({"error": str(e)})