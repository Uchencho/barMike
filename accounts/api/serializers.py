from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','email','username', 'first_name',
            'last_name','phone_number', 'is_active',
            'house_add','last_login',
        ]