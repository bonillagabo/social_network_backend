from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from .models import User
from .serializers import UserSerializer
from .helpers.encrypt_password import hash_md5
from .decorators import validate_jwt


@api_view(["POST"])
def createUser(request):
    try:
        password_encrypted = hash_md5(request.data["password"])
        request.data["password"] = password_encrypted
    except KeyError:
        pass

    serializer = UserSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except serializers.ValidationError as e:
        for field, error_message in e.detail.items():
            error_message = str(error_message[0])
            if (
                error_message == "user with this username already exists."
                or error_message == "user with this email already exists."
            ):
                return Response(status=400, data="Email or Username is alredy in use")
        return Response(status=400, data="Invalids fields")

    serializer.save()
    return Response(status=200, data="User registered")


@api_view(["GET"])
@validate_jwt
def getUser(request, username):
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(data={"The user does not exists"}, status=400)
