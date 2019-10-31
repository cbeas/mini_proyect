from django.db import models


class Subscriber(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField() 