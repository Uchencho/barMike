from rest_framework import serializers

from accounts.models import User
from enquiry.models import Enquiry


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','email','username', 'password', 'first_name',
            'last_name','phone_number', 'is_active', 'is_superuser',
            'house_add','last_login',
        ]



class AdminEnquirySerializer(serializers.ModelSerializer):
    user        = serializers.SerializerMethodField(read_only=True)
    created     = serializers.SerializerMethodField(read_only=True)
    updated     = serializers.SerializerMethodField(read_only=True)

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
        return obj.user.username

    def get_created(self, obj):
        return obj.created.strftime("%d-%b-%Y %H:%M")

    def get_updated(self, obj):
        return obj.updated.strftime("%d-%b-%Y %H:%M")