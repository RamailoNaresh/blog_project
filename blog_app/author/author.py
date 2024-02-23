from .accessor import AuthorAccess


class Author:

    @staticmethod
    def get_all_author():
        data = AuthorAccess.get_all_author()
        return data
    
    @staticmethod
    def get_author_by_id(id):
        data = AuthorAccess.get_author_by_id(id)
        if data:
            return data
        raise Exception("Data not found")
    
    @staticmethod
    def delete_author(id):
        data = AuthorAccess.get_author_by_id(id)
        if data is None:
            raise Exception("Data not found")
        AuthorAccess.delete_author(id)
