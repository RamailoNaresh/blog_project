from .accessor import CategoryAccess


class Category:

    @staticmethod
    def get_all_category():
        data = CategoryAccess.get_all_category()
        if data is not None:
            return data
        raise ValueError("No data available")
    

    @staticmethod
    def get_category_by_id(id):
        data = CategoryAccess.get_category_by_id(id)
        if data:
            return data
        raise ValueError("Data not found")

    @staticmethod
    def delete_category(id):
        data = CategoryAccess.get_category_by_id(id)
        if data is None:
            raise ValueError("Data not found")
        CategoryAccess.delete_category(id)

