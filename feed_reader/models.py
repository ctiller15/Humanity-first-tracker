from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    last_updated = models.DateTimeField()

class Entry(models.Model):
    title = models.CharField(max_length=300)
    link = models.CharField(max_length=300, unique=True)
    link_dirty = models.CharField(max_length=400, unique=True)
    summary = models.CharField(max_length=500)
    published = models.DateTimeField()
    updated = models.DateTimeField()
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
