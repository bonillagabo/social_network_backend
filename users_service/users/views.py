from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
from .helpers.encrypt_password import hash_md5


@api_view(["POST"])
def createUser(request):
    try:
        password_encrypted = hash_md5(request.data["password"])
        request.data["password"] = password_encrypted
    except KeyError:
        pass

    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=400, data="Invalids fields")

    request_email = request.data.get("email")
    email_exists = User.objects.filter(email=request_email).exists()
    request_username = request.data.get("username")
    username_exists = User.objects.filter(username=request_username).exists()
    if not username_exists and not email_exists:
        serializer.save()
        return Response(status=200, data="User registered")

    return Response(status=400, data="Email or Username is alredy in use")


@api_view(["GET"])
def getUser(request, username):
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(data={"The user does not exists"}, status=400)
