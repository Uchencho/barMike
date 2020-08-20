from rest_framework import generics, permissions

from .serializers import UserAdminSerializer
from accounts.models import User

class AllUsers(generics.ListAPIView):
    queryset                = User.objects.all()
    serializer_class        = UserAdminSerializer
    permission_classes      = [permissions.IsAdminUser]


class DeleteUser(generics.DestroyAPIView):
    queryset                = User.objects.all()
    serializer_class        = UserAdminSerializer
    permission_classes      = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)