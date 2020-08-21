from django.urls import path

from .views import AllUsers, DeleteUser, AllQuestions, EditQuestionBackOfficeView

app_name = "backoffice"

urlpatterns = [
    path('users', AllUsers.as_view(), name='users'),
    path('users/<int:pk>', DeleteUser.as_view(), name='deleteUser'),
    path('questions', AllQuestions.as_view(), name='questions'),
    path('questions/<int:pk>', EditQuestionBackOfficeView.as_view(), name='editQuestion'),
]