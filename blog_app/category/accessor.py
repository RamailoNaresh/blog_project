from blog_app.models import Category

class CategoryAccess:

    @staticmethod
    def get_all_category():
        return Category.objects.all()
    
    @staticmethod
    def get_category_by_id(id):
        return Category.objects.filter(id = id).first()
    
    @staticmethod
    def create_category(title, description):
        Category.objects.create(title = title, description = description)

    @staticmethod
    def delete_category(id):
        category = CategoryAccess.get_category_by_id(id)
        category.delete()
    
