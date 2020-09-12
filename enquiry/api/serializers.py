from rest_framework import serializers
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr, Point

from enquiry.models import Enquiry, UserLocation


class ListEnquirySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Enquiry
        fields =    [
                    'id',
                    'user', 
                    'question', 
                    'created', 
                    'updated', 
                    'answered']

    def get_user(self, obj):
        context = self.context['request']
        return context.user.username


class UserLocationSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserLocation
        fields =    [
                    'id',
                    'name',
                    'location',
                    'address',
                    'city',
                    'distance'
                    ]

    def get_name(self, obj):
        return obj.name.email

    def get_distance(self, obj):
        longitude = 50.453647
        latitude = -8.567856

        user_location = Point(longitude, latitude, srid=4326)
        return Distance(obj.location, user_location)


class CreateEnquirySerializer(ListEnquirySerializer):

    def create(self, validated_data):
        context = self.context['request']

        enq_obj = Enquiry(
            user=context.user,
            question=validated_data.get("question")
        )
        enq_obj.save()

        return enq_obj