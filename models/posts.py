class Post():
    """creating Post class"""
    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.

    def __init__(self, id, user_id, category_id, title, publication_date, content):
        self.id = id
        self.title = title
        self.user_id = user_id
        self.category_id = category_id
        self.publication_date = publication_date
        self.content = content
