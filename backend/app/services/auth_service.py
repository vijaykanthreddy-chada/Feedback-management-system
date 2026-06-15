from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.config.database import db
from app.models.user import User, UserRole


def register_user(data):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not name or not email or not password or not role:
        return {"error": "Name, email, password and role are required"}, 400

    if role not in [r.value for r in UserRole]:
        return {"error": "Invalid role"}, 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"error": "Email already registered"}, 409

    new_user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role=UserRole(role)
    )

    db.session.add(new_user)
    db.session.commit()

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role.value
        }
    }, 201


def login_user(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"error": "Invalid email or password"}, 401

    if not check_password_hash(user.password_hash, password):
        return {"error": "Invalid email or password"}, 401

    access_token = create_access_token(
    identity=str(user.id),
    additional_claims={
        "role": user.role.value,
        "email": user.email
    },
    expires_delta=timedelta(days=1)
)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value
        }
    }, 200