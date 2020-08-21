from django.urls import path

from .views import AllUsers, DeleteUser, AllQuestions

app_name = "backoffice"

urlpatterns = [
    path('users', AllUsers.as_view(), name='users'),
    path('users/<int:pk>', DeleteUser.as_view(), name='deleteUser'),
    path('questions', AllQuestions.as_view(), name='questions'),
]