import csv
from .category import Category
from rest_framework.response import Response
from .serializers import CategorySerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from blog_app.services.tokens import get_logged_user
from blog_app.api import api
from blog_app.api.response_builder import ResponseBuilder
from blog_app.shared.pagination import paginate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from blog_app.services.logger import logger_info, logger_warning

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_category(request):
    response_builder = ResponseBuilder()
    try:
        data = Category.get_all_category()
        categories, page_info = paginate(data, request)
        serializer = CategorySerializer(categories, many = True)
        logger_info.info("category fetched")
        return response_builder.get_200_success_response("Data fetched",page_info, serializer.data)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_category_by_id(request, id):
    response_builder = ResponseBuilder()
    try:
        data = Category.get_category_by_id(id)
        serializer = CategorySerializer(data)
        logger_info.info("category fetched")
        return response_builder.get_200_success_response("Data fetched", serializer.data)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
        


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_category(request):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin":
            data = JSONParser().parse(request)
            serializer = CategorySerializer(data =data)
            if serializer.is_valid():
                serializer.save()
                logger_info.info(f"category created")
                return response_builder.get_201_success_response("Category Successfully created", serializer.data)
            logger_warning.warning(serializer.errors)
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
        logger_warning.warning(f"Access denied {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_category(request, id):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin":
            data = JSONParser().parse(request)
            obj = Category.get_category_by_id(id)
            serializer = CategorySerializer(obj,data=data, partial = True)
            if serializer.is_valid():
                serializer.save()
                logger_info.info(f"category updated")
                return response_builder.get_200_success_response("Category Successfully updated", serializer.data)
            logger_warning.warning(serializer.errors)
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
        logger_warning.warning(f"Access denied {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))




@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_category(request, id):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin":
            Category.delete_category(id)
            logger_info.info(f"category deleted")
            return response_builder.get_201_success_response("Category Successfully deleted")
        logger_warning.warning(f"Access denied {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def create_category_using_csv(request):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin":
            logger_info.info("admin posting category")
            uploaded_file = request.FILES.get("file_path")
            logger_info.info("File impoerted")
            if uploaded_file is not None:
                file_contents = uploaded_file.read().decode("utf-8")
                datas = list(csv.DictReader(file_contents.splitlines()))
                error = {}
                error_data = []
                added_data = []
                for data in datas:
                    serializer = CategorySerializer(data =data)
                    if serializer.is_valid():
                        serializer.save()
                        logger_info.info(f"category created")
                        added_data.append(serializer.data)
                    else:
                        error_data.append(data)
                if len(error_data) != 0:
                    error["error_message"] = "Listed data are already in database"
                    error["data"] = error_data
                return response_builder.get_200_uploaded_data_from_csv(api.ADDED_DATA,error, added_data)
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "File is required")
        logger_warning.warning(f"Access denied {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    


@api_view(["GET"])
def export_categories(request):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin":
            data = Category.get_all_category()
            serializer = CategorySerializer(data, many = True)
            fields_name = ["id","created_at", "updated_at","title", "description"]
            with open("datas.csv", "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields_name)
                writer.writeheader()
                for row in serializer.data:
                    writer.writerow(row)
            return response_builder.get_200_login_success_response("Data successfully added in data.csv file")
        logger_warning.warning(f"Access denied {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(str(e))
        return response_builder.get_400_bad_request_response(api.CATEGORY_NOT_FOUND, str(e))
    except Exception as e:
        logger_warning.warning(str(e))
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))