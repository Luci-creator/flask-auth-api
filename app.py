from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

with app.app_context():
    db.create_all()


@app.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User exists"}), 409

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"}), 201


@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"error": "Account disabled"}), 403

    access_token = create_access_token(identity=user.id)

    return jsonify({"access_token": access_token}), 200


@app.route("/me", methods=["GET"])
@jwt_required()
@limiter.limit("20 per minute")
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    return jsonify({
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active
    })


@app.route("/me", methods=["PUT"])
@jwt_required()
@limiter.limit("10 per minute")
def update_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    data = request.get_json()

    if "password" in data:
        user.set_password(data["password"])

    db.session.commit()

    return jsonify({"message": "Account updated"})


@app.route("/me", methods=["DELETE"])
@jwt_required()
@limiter.limit("5 per minute")
def deactivate():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    user.is_active = False
    db.session.commit()

    return jsonify({"message": "Account deactivated"})


if __name__ == "__main__":
    app.run(debug=True)

