from .category import Category
from rest_framework.response import Response
from .serializers import CategorySerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
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
    data = Category.get_all_category()
    categories, page_info = paginate(data, request)
    serializer = CategorySerializer(categories, many = True)
    logger_info.info("category fetched")
    return response_builder.get_200_success_response("Data fetched",page_info, serializer.data)


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