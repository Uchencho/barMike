from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.geos import fromstr

from enquiry.models import Enquiry, UserLocation
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


class AddLocation(APIView):

    def post(self, request):

        lon     = request.data.get("longitude", None)
        lat     = request.data.get("latitude", None)
        address = request.data.get("address", None)
        city    = request.data.get("city", None)

        if not lat or not lon or not address or not city:
            return Response({"message" : "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)

        location = fromstr(f"POINT({lon} {lat})", srid=4326)

        UserLocation.objects.create(
            name = request.user,
            address = address,
            city = city,
            location = location
        )

        return Response({"message" : "created successfully"}, status=status.HTTP_200_OK)

