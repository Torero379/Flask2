from marshmallow import EXCLUDE
from api import ma
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema
from marshmallow.validate import Length

def rating_validate(validate: int):
    return value in range(1,6)



class QuoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuoteModel
        dump_only = ("id")
        unknow = EXCLUDE
        load_instance = True

    id = ma.auto_field()
    text = ma.auto_field(required = True,validate= Length(min =3))
    author = ma.Nested(AuthorSchema(only= ("name","surname")))
    rating = ma.Integer(strict = True, validate= rating_validate)
quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True, exclude = ["author"])