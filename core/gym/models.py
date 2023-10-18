from django.db import models
from django.conf import settings


class Gym(models.Model):
    '''Model for gym details.'''
    name = models.CharField(max_length=255, unique=True)
    number = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    days_closed = models.CharField(max_length=255)
    hour_open = models.TimeField()
    hour_close = models.TimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='review'
        )
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return str(self.author)


class Social(models.Model):
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='social'
        )
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.name
