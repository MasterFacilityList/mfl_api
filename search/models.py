from django.db import models


class IndexErrorQueue(models.Model):
    object_pk = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    success = models.BooleanField(default=False)
    retries = models.IntegerField(default=0)
