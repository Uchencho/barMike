from rest_framework import generics

from enquiry.models import Enquiry
from .serializers import CreateEnquirySerializer

class AskQuestionAPIView(generics.CreateAPIView):

    serializer_class = CreateEnquirySerializer
    
    def get_queryset(self):
        Enquiry.objects.filter(user__iexact=self.request.user)

    def get_serializer_context(self, *args, **kwargs):
        return {"request" : self.request}