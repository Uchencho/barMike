from rest_framework import generics, permissions

from accounts.api.serializers import UserSerializer
from accounts.models import User

class AllUsers(generics.ListAPIView):
    queryset                = User.objects.all()
    serializer_class        = UserSerializer
    permission_classes      = [permissions.IsAdminUser]
