from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance

from cloudinary import uploader, utils

from enquiry.models import Enquiry, UserLocation
from accounts.models import User
from .serializers import CreateEnquirySerializer, ListEnquirySerializer, UserLocationSerializer

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

        # Sample payload
        # {
        #     "latitude" : 30.4260072,
        #     "longitude" : -9.6199602,
        #     "address" : "kodesho street",
        #     "city" : "lagos"
        # }

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


class GetDistance(generics.ListAPIView):

    serializer_class        = UserLocationSerializer

    def get_queryset(self):
        longitude = 50.453647
        latitude = -8.567856

        user_location = Point(longitude, latitude, srid=4326)
        return UserLocation.objects.annotate(distance=Distance('location',
                                                user_location)).order_by('distance')


class UploadView(APIView):

    parser_classes = [MultiPartParser, JSONParser]

    @staticmethod
    def post(request):
        """
        The static method prevents post from accessing other methods in the class
        """
        the_file = request.data.get('picture', None)
        cost     = request.data.get('cost', None)

        filename = str(the_file).split(".")[0]
        file_ext = str(the_file).split(".")[1]

        if not the_file:
            return Response({"picture":"No image was sent"}, status=status.HTTP_400_BAD_REQUEST)

        #This process takes time, if url is not needed immediately, run concurrently maybe?
        try:
            upload_data = uploader.upload(the_file, public_id=filename)
            return Response({"status":"success",
                            "cost" : cost,
                            "created_at" : upload_data["created_at"],
                            "secure_url" : upload_data["secure_url"],
                            "url" : upload_data["url"],
                            "file_name" : filename,
                            "file_extension" : file_ext}, status=201)
        
        except Exception as e:
            print("\n\n", "Error occured in sending image: ", e, "\n\n")
            return Response({"message" : "Could not send image to cloudinary"},
                                status=status.HTTP_400_BAD_REQUEST)


class GetUploadedFile(APIView):

    def post(self, request):
        """
        Retrieve the url of an image stored on cloudinary
        """
        image_name      = request.data.get("image_name", None)

        if not image_name:
            return Response({"message":"Did not send any image name"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        link            = utils.cloudinary_url(image_name)
        return Response({"status" : "success", "link_url" : link[0]},
                            status=status.HTTP_200_OK)

