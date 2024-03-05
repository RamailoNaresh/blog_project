from rest_framework.response import Response
from blog_app.author.serializers import AuthorSerializer
from rest_framework.decorators import api_view
from blog_app.author.author import Author
from rest_framework.parsers import JSONParser
from blog_app.services.tokens import get_logged_user
from blog_app.util.password_encoder import validate_password
from blog_app.api.response_builder import ResponseBuilder
from blog_app.api import api
from blog_app.shared.pagination import paginate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from blog_app.services.logger import logger_info, logger_warning



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_author(request):
    try:
        response_builder = ResponseBuilder()
        user = get_logged_user(request.user.id)
        if user.role == "Admin":
            data = Author.get_all_author()
            paginated_authors, page_info = paginate(data, request)
            serializer = AuthorSerializer(paginated_authors, many = True)
            logger_info.info("data fetched")
            return response_builder.get_200_success_response("Data fetched",page_info, serializer.data)
        logger_warning.warning(f"Access denied for {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(f"Value Error occurred {str(e)}")
        return response_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND,str(e))
    except Exception as e:
        logger_warning.warning(f"Error occurred {str(e)}")
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_author_by_id(request, id):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin" or user.id == id:
            data = Author.get_author_by_id(id)
            serializer = AuthorSerializer(data)
            logger_info.info("data fetched")
            return response_builder.get_200_success_response("Data fetched", serializer.data)
        logger_warning.warning(f"Access denied for {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(f"Value Error occurred {str(e)}")
        return response_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND,str(e))
    except Exception as e:
        logger_warning.warning(f"Error occurred {str(e)}")
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_author(request, id):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin" or user.id == id:
            data = JSONParser().parse(request)
            obj = Author.get_author_by_id(id)
            serializer = AuthorSerializer(obj,data=data, partial = True)
            if serializer.is_valid():
                serializer.save()
                logger_info.info(f"User updated {obj.email}")
                return response_builder.get_200_success_response("Successfully Updated", serializer.data)
            logger_warning.warning(f"{serializer.errors}")
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
        logger_warning.warning(f"Access denied for {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(f"Value Error occurred {str(e)}")
        return response_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND,str(e))
    except Exception as e:
        logger_warning.warning(f"Error occurred {str(e)}")
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))



@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_author(request, id):
    response_builder = ResponseBuilder()
    try:
        user = get_logged_user(request.user.id)
        if user.role == "Admin" or user.id == id:
            Author.delete_author(id)
            logger_info.info(f"User deleted {user.email}")
            return response_builder.get_201_success_response("Data Successfully deleted")
        logger_warning.warning(f"Access denied for {user.email}")
        return response_builder.get_401_unauthorized_access_response(api.UNAUTHORIZED_ACCESS)
    except ValueError as e:
        logger_warning.warning(f"Value Error occurred {str(e)}")
        return response_builder.get_400_bad_request_response(api.AUTHOR_NOT_FOUND,str(e))
    except Exception as e:
        logger_warning.warning(f"Error occurred {str(e)}")
        return response_builder.get_500_server_error_response(api.SERVER_ERROR, str(e))
    
