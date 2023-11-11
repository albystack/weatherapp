from django.db import models
from django.contrib.auth.models import User

class WeatherData(models.Model):
    # Fields to store weather data, e.g., temperature, humidity, location, timestamp, etc.
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.location} - {self.timestamp}"

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Fields to store user preferences, e.g., units, notification settings, etc.
    units = models.CharField(max_length=10, default='Celsius')
    receive_notifications = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
