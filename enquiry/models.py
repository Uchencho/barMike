from django.db import models
from django.contrib.gis.db import models as gis_model

from accounts.models import User

class QuetionQuerySet(models.QuerySet):
    pass

class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuetionQuerySet(self.model, using=self._db)

class Enquiry(models.Model):

    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    question    = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    answered    = models.BooleanField(default=False)

    objects = QuestionManager()

    def __str__(self):
        return str(self.question)[:50]

    class Meta:
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"



class UserLocation(gis_model.Model):

    name        = gis_model.ForeignKey(User, on_delete=models.CASCADE)
    location    = gis_model.PointField()
    address     = gis_model.CharField(max_length=200)
    city        = gis_model.CharField(max_length=100)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name        = "User Location"
        verbose_name_plural = "Users' Location"

