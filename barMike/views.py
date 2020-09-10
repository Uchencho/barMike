from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import task_that_takes_time
from django.utils import timezone
import asyncio

loop = asyncio.get_event_loop()

class HealthCheck(APIView):
    def get(self, request):
        print("calling background task")
        loop.run_in_executor(None, task_that_takes_time)
        print("\n\nAlready called background")
        return Response({
            "message" : "Barister Mike working Effectively"
        })

