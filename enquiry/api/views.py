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


class EditQuestionAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ListEnquirySerializer

    def get_queryset(self):
        return Enquiry.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user,
                        question=serializer.validated_data.get('question'))

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)