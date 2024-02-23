from .category import Category
from rest_framework.response import Response
from .serializers import CategorySerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(["GET"])
def get_all_category(request):
    data = Category.get_all_category()
    serializer = CategorySerializer(data, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_category_by_id(request, id):
    try:
        data = Category.get_category_by_id(id)
        serializer = CategorySerializer(data)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(["POST"])
def create_category(request):
    try:
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data =data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "data successfully created", "data": data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["PUT", "PATCH"])
def update_category(request, id):
    try:
        data = JSONParser().parse(request)
        obj = Category.get_category_by_id(id)
        serializer = CategorySerializer(obj,data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




@api_view(["DELETE"])
def delete_category(request, id):
    try:
        Category.delete_category(id)
        return Response({"message": "Data successfully deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)