from rest_framework.views import APIView
from rest_framework import exceptions, status, generics
from rest_framework.response import Response
from django.conf import settings
import jwt, redis, json
from datetime import timedelta
from django.utils import timezone
from pyfcm import FCMNotification

from accounts.models import User
from .serializers import UserSerializer, UserRegisterSerializer, UpdateProfileSerializer
from .permissions import BasicToken
from .utils import generate_access_token, generate_refresh_token


#Connect to redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                    db=0)

class Login(APIView):
    permission_classes      = [BasicToken]
    authentication_classes  = []

    def get_serializer_context(self, *args, **kwargs):
        return {"request" : self.request}

    def post(self, request):
        email = request.data.get('email', "Not Sent")
        password = request.data.get('password', "Not Sent")
        response = Response()

        if email == "Not Sent" or password == "Not Sent":
            raise exceptions.AuthenticationFailed("Credentials not sent")

        #Check if username exists in redis
        try:
            available = redis_instance.get(email)
            if available and json.loads(available)['password'] == password:
                available = json.loads(available)
                response.set_cookie(key='refreshtoken', value=available['refresh_token'], httponly=True)
                available.pop('refresh_token')
                response.data = available
                return response
        except redis.exceptions.ConnectionError:
            pass

        user = User.objects.filter(email__iexact=email).first()
        if user == None or not user.check_password(password):
            raise exceptions.AuthenticationFailed("Credentials incorrect")

        user = User.objects.filter(email__iexact=email).first()
        user.last_login = timezone.now()
        user.save()

        # Push notification
        push_service = FCMNotification(api_key=settings.FCM_API_KEY)
        push_service.notify_topic_subscribers(topic_name="do.not.stress.me", message_body="from python version 2")
        
        serialized_user = UserSerializer(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        serialized_user['access_token'] = access_token
        response.data = serialized_user

        # Add it to redis
        try:
            serialized_user['refresh_token'] = refresh_token
            serialized_user['password'] = password
            redis_instance.set(email, json.dumps(serialized_user), ex=timedelta(hours=2))
        except redis.exceptions.ConnectionError:
            pass
        response.data.pop("refresh_token")
        response.data.pop("password")
        return response


class RefreshToken(APIView):
    permission_classes      = []
    authentication_classes  = []

    def post(self, request):
        refresh_token = request.COOKIES.get('refreshtoken', "None")
        if refresh_token == "None":
            raise exceptions.AuthenticationFailed("Authentication Credentials were not provided")

        try:
            payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET,
                                    algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Expired Refresh Token, please login again")
        except:
            raise exceptions.AuthenticationFailed("Can't decode, please login again")

        user = User.objects.filter(id=payload.get("user_id")).first()
        if user == None or not user.is_active:
            raise exceptions.AuthenticationFailed("User not found")

        new_access_token = generate_access_token(user)
        return Response({"access_token": new_access_token})


class RegisterAPIView(generics.CreateAPIView):
    queryset                = User.objects.all()
    serializer_class        = UserRegisterSerializer
    permission_classes      = [BasicToken]
    authentication_classes  = []


class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("refreshtoken")
        response.data = {"message" : "logged out successfully"}
        response.status_code = status.HTTP_204_NO_CONTENT
        return response


class UpdateProfileView(generics.RetrieveUpdateAPIView):

    serializer_class        =  UpdateProfileSerializer

    def get_queryset(self):
        return User.objects.filter(username__iexact=self.request.user.username)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
