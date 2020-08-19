from rest_framework import generics

from enquiry.models import Enquiry
from accounts.models import User
from .serializers import CreateEnquirySerializer, ListEnquirySerializer

class AskQuestionAPIView(generics.CreateAPIView):

    serializer_class = CreateEnquirySerializer
    
    def get_queryset(self):
        Enquiry.objects.filter(user__iexact=self.request.user)

    def get_serializer_context(self, *args, **kwargs):
        return {"request" : self.request}


class AllQuestionAPIView(generics.ListAPIView):

    serializer_class = ListEnquirySerializer

    def get_queryset(self):
        return Enquiry.objects.filter(user=self.request.user)

    def get_serializer_context(self, *args, **kwargs):
        return {"request" : self.request}