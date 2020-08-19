from django.contrib import admin
from django.urls import path, include

from accounts.api.views import HealthCheck

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.api.urls', namespace='api-accounts')),
    path('api/enquiry/', include('enquiry.api.urls', namespace='api-enquiry')),
    path('healthcheck', HealthCheck.as_view()),
]
