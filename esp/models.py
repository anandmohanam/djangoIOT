from django.db import models
from datetime import datetime

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature_C = models.IntegerField()
    humidity = models.IntegerField()

    def __str__(self):
        # Convert the timestamp to 12-hour format with AM/PM
        formatted_time = self.timestamp.strftime('%I:%M %p, %d-%b-%Y')
        return f"Temp: {self.temperature_C}°C, Humidity: {self.humidity}%, Time: {formatted_time}"


class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name

class Notify(models.Model):
    counter = models.IntegerField(default=0)

    def __str__(self):
        return f"Notify {self.counter}"