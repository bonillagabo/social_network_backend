import jwt
from flask import jsonify
from auth.models import User
from datetime import datetime, timedelta
from auth import app


def login(email_request, password_request):
    user = (User.query.filter(User.email == email_request).first()).as_dict()
    user_email = user["email"]
    user_password = user["password"]

    if email_request == user_email and password_request == user_password:
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        token = jwt.encode(
            {"email": email_request, "exp": expiration_time},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401


def validate_token(token):
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        email = payload.get("email")

        return jsonify({"email": email}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
