from author import Author
from schema import AuthorSchema


author = Author(1, "Alex", "alex5@mail.ru")

authors = [
Author("1", "Alex"),
Author("1", "Ivan"),
Author("1", "Tom")
]
author_schema = AuthorSchema()
result = author_schema.dump(authors, many=True)
        
print(type(result), result)