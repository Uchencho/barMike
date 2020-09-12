from django.urls import path, include

from .views import ( 
                    AskQuestionAPIView, AllQuestionAPIView,
                    EditQuestionAPIView, AddLocation)

app_name = "enquiry"

urlpatterns = [
    path('ask', AskQuestionAPIView.as_view(), name='ask'),
    path('location', AddLocation.as_view(), name='location'),
    path('myenquiries', AllQuestionAPIView.as_view(), name='allQuestions'),
    path('myenquiries/<int:pk>', EditQuestionAPIView.as_view(), name='editQuestion'),
]