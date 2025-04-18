from django.db import models


# Create your models here.

class Setting(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=2047, default=0)

    def __str__(self):
        return self.name

class Context(models.Model):
    slug = models.CharField(max_length=255, unique=True)
    value = models.TextField(default="")

    def __str__(self):
        return self.slug
