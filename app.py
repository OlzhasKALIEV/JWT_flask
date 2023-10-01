from flask import Flask
from flask import jsonify
from flask import request
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from database import db, Users
from schema import schema_register

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


@app.route("/register/", methods=["POST"])
def register_users():
    try:
        register = request.get_json()
        validate(instance=register, schema=schema_register)
        user = Users.query.filter_by(username=register["username"]).first()
        if user:
            return jsonify({'message': 'User already exists'}), 200
        else:
            db.create_all()
            new_users = Users(username=register["username"], password=register["password"])
            db.session.add(new_users)
            db.session.commit()
            return jsonify({'message': 'Users added successfully'}), 200
    except ValidationError as ex:
        return {
            "errors": ex.message
        }, 400


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route("/hello/", methods=["GET"])
@jwt_required()
def hello():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify({"dsfsd": "hello"}), 200


if __name__ == '__main__':
    app.run(debug=True)
