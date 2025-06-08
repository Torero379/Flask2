from flask import jsonify, request
from api import app, db
from api.models.user import UserModel
from api.schemas.user import UserSchema, user_schema


@app.get('/users/<int:user_id>')
def get_user_by_id(user_id: int):
    user = db.get_or_404(UserModel, user_id, description=f"User with id={user_id} not found")
    return jsonify(user_schema.dump(user)), 200
    
 
@app.get('/users')
def get_users():
    users = db.session.scalars(db.select(UserModel)).all()
    return jsonify(user_schema.dump(users, many=True)), 200


@app.post("/user")
def create_user():
    user = UserSchema.loads(request.data)  
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201

