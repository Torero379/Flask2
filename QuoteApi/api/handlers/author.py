from api import db, app
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.author import author_schema, authors_schema, change_author_schema
from marshmallow import ValidationError, EXCLUDE

@app.post("/authors")
def create_author():
    try:
        # 1. Get raw bytes
        # print(f'{request.data =})
        # 2. Load bytes to dict
        # author_data = author_schema.loads(request.data)
        # print(f'{author_data = }, {type(author_data)})
        # 3. Create new AuthorModel instance via dict
        # author = AuthorModel(**author_data)
        author = author_schema.loads(request.data)  # get_data() return raw bytes
        db.session.add(author)
        db.session.commit()
    except ValidationError as ve:
        abort(400, f"Validation error: {str(ve)}")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    # db instance -> dict -> json
    return jsonify(author_schema.dump(author)), 201

@app.get("/authors")
def get_authors():
    """ Функция возвращает все цитаты из БД. """
    authors_db = db.session.scalars(db.select(AuthorModel)).all()
    
    # Формируем список словарей
    #quotes = []
    #for quote in quotes_db:
    #    quotes.append(quote.to_dict())
    #return jsonify(quotes), 200
    return jsonify(authors_schema.dump(authors_db)),200

@app.get("/authors/<int:author_id>")
def get_author_by_id(author_id: int):
    """ Return quote by id from db."""
    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"author with id={author_id} not found")
    #return jsonify(author.to_dict()), 200
    return jsonify(author_schema.dump(author)),200



@app.put("/authors/<int:authors_id>")
def edit_authors(authors_id: int):
    new_data = request.json
    author = db.get_or_404(entity=AuthorModel, ident=authors_id, description=f"author with id={authors_id} not found")
    for key_as_attr, value in new_data.items():
        setattr(author, key_as_attr, value)
    db.session.commit()
    return jsonify(author.to_dict()), 200   


@app.route("/authors/<int:authors_id>", methods=['DELETE'])
def delete_author(authors_id):
    """Delete quote by id """
    author = db.get_or_404(entity=AuthorModel, ident=authors_id, description=f"Author with id={authors_id} not found")
    db.session.delete(author)
    try:
        db.session.commit()
        return jsonify({"message": f"Quote with id {authors_id} has deleted."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")
