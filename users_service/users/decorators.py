from functools import wraps
from rest_framework.response import Response
from rest_framework import status
import requests
import jwt


def validate_jwt(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        token = args[0].headers.get("Authorization")

        if not token:
            return Response(
                {"error": "Token de autenticación no proporcionado"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            response = requests.post(
                "http://auth:8001/validate_token", json={"token": token}
            )
            response.raise_for_status()
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Expired token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except jwt.InvalidTokenError:
            return Response(
                {"error": "Invalid Token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except requests.RequestException as e:
            return Response(
                {"error": f"Error on external service: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return view_func(*args, **kwargs)

    return wrapped_view
