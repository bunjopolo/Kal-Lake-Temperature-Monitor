from django.db import models

# Create your models here.

class temperatureReading(models.Model):
    temp = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['time']),
        ]