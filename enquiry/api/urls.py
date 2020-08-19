from django.urls import path, include

from .views import AskQuestionAPIView, AllQuestionAPIView

app_name = "enquiry"

urlpatterns = [
    path('ask', AskQuestionAPIView.as_view(), name='ask'),
    path('myenquiries', AllQuestionAPIView.as_view(), name='allQuestions'),
]