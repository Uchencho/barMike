from django.urls import path, include

from .views import ( 
                    AskQuestionAPIView, AllQuestionAPIView,
                    EditQuestionAPIView, AddLocation, 
                    GetDistance, UploadView)

app_name = "enquiry"

urlpatterns = [
    path('ask', AskQuestionAPIView.as_view(), name='ask'),
    path('myenquiries', AllQuestionAPIView.as_view(), name='allQuestions'),
    path('myenquiries/<int:pk>', EditQuestionAPIView.as_view(), name='editQuestion'),

    path('location', AddLocation.as_view(), name='location'),
    path('distance', GetDistance.as_view(), name='distance'),
    path('upload', UploadView.as_view(), name='cloudinary-upload'),
]