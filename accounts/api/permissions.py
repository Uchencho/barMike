from rest_framework.authentication import get_authorization_header
from rest_framework import permissions

class BasicToken(permissions.BasePermission):
    message = "No token was passed"

    def has_permission(self, request, view):
        token = "7f7c3466391e87a6bffc501dd49cbcbbfe3743c1dd1489859378e61ba831a3d6"
        try:
            in_token = get_authorization_header(request).decode('utf-8').split(" ")[1]
        except IndexError:
            return False
        if token != in_token:
            return False
        return True