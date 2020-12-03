from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Appointment

# NIE DZIAŁA
# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
#         model.email = model.username

class DateInput(forms.DateInput):
    input_type = 'date'

class AppointmentForm(ModelForm):
    start_hour = start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'time'}))
    end_hour = start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'time'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Appointment
        fields = ['title', 'start_date', 'start_hour', 'end_hour', 'patient', 'doctor']
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'