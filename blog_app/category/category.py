from .accessor import CategoryAccess


class Category:

    @staticmethod
    def get_all_category():
        return CategoryAccess.get_all_category()
    

    @staticmethod
    def get_category_by_id(id):
        data = CategoryAccess.get_category_by_id(id)
        if data:
            return data
        raise Exception("Data not found")

    @staticmethod
    def delete_category(id):
        data = CategoryAccess.get_category_by_id(id)
        if data is None:
            raise Exception("Data not found")
        CategoryAccess.delete_category(id)

