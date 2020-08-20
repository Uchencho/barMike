from rest_framework import serializers

from accounts.models import User


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','email','username', 'password', 'first_name',
            'last_name','phone_number', 'is_active', 'is_superuser',
            'house_add','last_login',
        ]