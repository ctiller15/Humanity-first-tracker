from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    last_updated = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

class Entry(models.Model):
    title = models.CharField(max_length=300)
    site_url = models.CharField(max_length=300, null=True)
    link = models.CharField(max_length=300, unique=True)
    link_dirty = models.CharField(max_length=400, unique=True)
    summary = models.CharField(max_length=500)

    og_image = models.CharField(max_length=500, null=True)
    og_title = models.CharField(max_length=300, null=True)
    og_site_name = models.CharField(max_length=100, null=True)

    published = models.DateTimeField()
    updated = models.DateTimeField()
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    hidden = models.BooleanField(default=False)
