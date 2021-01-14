from django.contrib import admin
from .models import Appointment
from .models import UserProfile
from .models import AppointmentNote

# Register your models here.
admin.site.register(Appointment)
admin.site.register(UserProfile)
admin.site.register(AppointmentNote)