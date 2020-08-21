from rest_framework import generics, permissions

from .serializers import UserAdminSerializer, AdminEnquirySerializer
from accounts.models import User
from enquiry.models import Enquiry

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


class AllQuestions(generics.ListAPIView):
    queryset                = Enquiry.objects.all()
    serializer_class        = AdminEnquirySerializer
    permission_classes      = [permissions.IsAdminUser]