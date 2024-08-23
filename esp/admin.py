from django.contrib import admin
from esp.models import SensorData, ContactForm, Notify

# Register your models here.
admin.site.register(SensorData)
admin.site.register(ContactForm)
admin.site.register(Notify)