from .accessor import PostAccess
from slugify import slugify
from blog_app.category.category import CategoryService


class PostService:

    @staticmethod
    def get_all_post():
        datas = PostAccess.get_all_post()
        return datas
    
    @staticmethod
    def get_post_by_id(id):
        data =PostAccess.get_post_by_id(id)
        if data:
            return data
        raise Exception("No data available")
    

    @staticmethod
    def get_post_by_author(id):
        data = PostAccess.get_post_by_author(id)
        if data:
            return data
        raise Exception("No data available")
    
    @staticmethod
    def get_post_by_slug(slug):
        data = PostAccess.get_post_by_slug(slug)
        if data:
            return data
        raise Exception("No data available")


    @staticmethod
    def create_post(data):
        data["slug"] = slugify(data["title"])
        return data

    @staticmethod
    def get_post_by_category(id):
        data = PostAccess.get_post_by_category(id)
        if data:
            return data
        raise Exception("No data available")

    @staticmethod
    def delete_post(id):
        data = PostAccess.get_post_by_id(id)
        if not data:
            raise Exception("Data doesn't exists")
        PostAccess.delete_post(id)

