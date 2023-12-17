from flask import Blueprint, request
from helpers.encrypt_password import hash_md5
from auth.controllers import login, validate_token

auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.route("/login", methods=["POST"])
def login_route():
    email_request = request.json.get("email")
    password_request = hash_md5(request.json.get("password"))
    return login(email_request, password_request)


@auth_routes.route("/validate_token", methods=["POST"])
def validate_token_route():
    token = request.json.get("token")
    return validate_token(token)
