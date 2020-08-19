from django.urls import path, include

from .views import AskQuestionAPIView

app_name = "enquiry"

urlpatterns = [
    path('ask', AskQuestionAPIView.as_view(), name='ask'),
]