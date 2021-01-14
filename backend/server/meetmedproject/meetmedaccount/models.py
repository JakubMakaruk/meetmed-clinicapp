from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.urls import reverse

def defaultTitle():
    id=''
    try:
        id = str(Appointment.objects.order_by('-id').first().id + 1)
    except:
        id = '1'
    return 'Wizyta ' + id
def defaultDoneClass():
    return ''

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(null=True, blank=True, max_length=9)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " | " + self.phone

# WIZYTA U LEKARZA
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default=defaultTitle)
    description = models.CharField(max_length=480, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    date_reserved = models.DateTimeField(null=True, blank=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+', blank=True)
    done = models.CharField(max_length=30, default=defaultDoneClass)

    def __str__(self):
        if self.patient:
            return self.title + " | " + self.patient.first_name + " " + self.patient.last_name
        return self.title + " |"

class AppointmentNote(models.Model):
    id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=1500)
    def __str__(self):
        return self.appointment.title

    

