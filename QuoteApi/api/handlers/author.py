from api import db, app
from flask import request, abort, jsonify
from api.models.author import AuthorModel


@app.post("/authors")
def create_author():
    author_data = request.json
    try:
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
    quotes_db = db.session.scalars(db.select(AuthorModel)).all()
    
    # Формируем список словарей
    quotes = []
    for quote in quotes_db:
        quotes.append(quote.to_dict())
    return jsonify(quotes), 200

@app.get("/author/<int:author_id>")
def get_author_by_id(author_id: int):
    """ Return quote by id from db."""
    quote = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Quote with id={author_id} not found")
    return jsonify(quote.to_dict()), 200


