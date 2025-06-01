from marshmallow import Schema, fields


class AuthorSchema(Schema):
    id=fields.Integer(strict=True,dump_only=True)
    name = fields.String(required=True, error_messages={"required ":"field'name'" })
    email = fields.Email(required=True, error_messages={"required ":"field'email'" })
    surname = fields.String()
