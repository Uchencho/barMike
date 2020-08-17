from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.response import Response

from accounts.models import User
from .serializers import UserSerializer
from .permissions import BasicToken
from .utils import generate_access_token, generate_refresh_token

class Login(APIView):
    permission_classes      = [BasicToken]
    authentication_classes  = []

    def post(self, request):
        email = request.data.get('email', "Not Sent")
        password = request.data.get('password', "Not Sent")
        response = Response()

        if email == "Not Sent" or password == "Not Sent":
            raise exceptions.AuthenticationFailed("Credentials not sent")

        user = User.objects.filter(email__iexact=email).first()
        if user == None or not user.check_password(password):
            raise exceptions.AuthenticationFailed("Credentials incorrect")

        serialized_user = UserSerializer(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        serialized_user['access_token'] = access_token
        response.data = serialized_user
        return response


class HealthCheck(APIView):
    def get(self, request):
        return Response({
            "message" : "Barister Mike workorking Effectively"
        })