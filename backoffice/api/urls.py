from django.urls import path

from .views import AllUsers

app_name = "backoffice"

urlpatterns = [
    path('users', AllUsers.as_view(), name='users'),
]