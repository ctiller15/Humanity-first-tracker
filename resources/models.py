from django.db import models

class Resource(models.Model):
    title = models.CharField(max_length=300)
    summary = models.CharField(max_length=300)
    link = models.CharField(max_length=200)
    order = models.IntegerField()
    hidden = models.BooleanField(default=False)
