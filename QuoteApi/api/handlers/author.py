from api import db, app
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.author import author_schema, authors_schema


@app.post("/authors")
def create_author():
    author_data = request.json

    try:
        if "surname" not in author_data:
            author_data["surname"]="-" 
        author = AuthorModel(**author_data)
        db.session.add(author)
        db.session.commit()
    except TypeError:
        abort(400, f"Invalid data. Required: <name>. Received: {', '.join(author_data.keys())}")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    return jsonify(author.to_dict()), 201
   


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
    quote = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"author with id={author_id} not found")
    return jsonify(quote.to_dict()), 200



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
