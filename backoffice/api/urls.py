from django.urls import path

from .views import AllUsers, DeleteUser

app_name = "backoffice"

urlpatterns = [
    path('users', AllUsers.as_view(), name='users'),
    path('users/<int:pk>', DeleteUser.as_view(), name='deleteUser'),
]