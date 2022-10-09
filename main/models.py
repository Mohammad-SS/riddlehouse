from django.db import models


# Create your models here.

class Setting(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=127, default=0)

    def __str__(self):
        return self.name
