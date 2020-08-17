from django.urls import path, include

from .views import Login

app_name = "accounts"

urlpatterns = [
    path('login', Login.as_view(), name='login'),
]