from django.urls import path, include

from .views import Login, RefreshToken, RegisterAPIView

app_name = "accounts"

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('refresh', RefreshToken.as_view(), name='refresh'),
    path('register', RegisterAPIView.as_view(), name='register'),
]