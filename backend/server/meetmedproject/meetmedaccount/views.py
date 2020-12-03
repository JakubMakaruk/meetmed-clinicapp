from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.core import serializers

# Create your views here.
from .models import *
# from .forms import CreateUserForm
from .forms import AppointmentForm

from .decorators import unauthenticated_user, allowed_users, patient_only

from .models import Appointment

from django.http import JsonResponse
import json

from django.http import HttpResponse

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('userhome')
        else:
            messages.error(request, "Niepoprawne dane!")
            return redirect('login')
    else:
        return render(request, 'login.html')

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if first_name == "" or last_name == "" or email == "" or password1 == "" or password2 == "":
            messages.error(request, "Wypełnij wszystkie pola!")
            return redirect('register')
        if email.find('@') == -1:
            messages.error(request, "Niepoprawny email!")
            return redirect('register')
        if password1 != password2:
            messages.error(request, "Hasła nie są podobne!")
            return redirect('register')
        if password1 == password2:
            if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
                messages.error(request, "Ten adres email już istnieje w bazie!")
                return redirect('register')
            else:
                user = User.objects.create_user(username=email, password=password1, email=email, first_name=first_name, last_name=last_name)
                group = Group.objects.get(name='Patient')
                user.groups.add(group)
                user.save()
                messages.success(request, "Utworzono konto!")
                return redirect('login')
        return redirect('/')

    else:
        return render(request, 'register.html')


@login_required(login_url='login')
@patient_only
def userhome(request):
    return render(request, 'userpanel.html')

def logout(request):
    auth.logout(request)
    return redirect('login')


# DOCTOR ---------------------------------------------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def doctorhome(request):
    context = {
        'appointments': Appointment.objects.all()
    }
    return render(request, 'doctorhome.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def doctortoday(request):
    today = datetime.date.today().strftime("%d.%m.%Y")
    today_appointments = None
    if request.is_ajax and request.method == 'POST':
        idDoneAppointment = request.POST['id'].replace('button:', '')
        currentAppointment = Appointment.objects.get(id=idDoneAppointment)
        print(currentAppointment)
        if currentAppointment.done == 'btn-info':
            print(currentAppointment.done)
            currentAppointment.done = 'btn-danger'
            print(currentAppointment.done)
            currentAppointment.save()
        elif currentAppointment.done == 'btn-danger':
            currentAppointment.done = 'btn-info'
            currentAppointment.save()
        return redirect('doctortoday')
    elif request.method == 'GET':
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

        try:
            today_appointments = Appointment.objects.filter(doctor=request.user, start_date__range=(today_min, today_max))
        except:
            today_appointments = None

    context = {
        'today': today,
        'appointments': today_appointments
    }
    return render(request, 'doctortoday.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def doctorcalendar(request):
    all_appointments = Appointment.objects.all()
    get_appointment_doctors = Appointment.objects.only('doctor')
    form = AppointmentForm()

    if request.method == 'POST' and "button-add" in request.POST:
        print(request.POST)
        print(request.headers)
        if Appointment.objects.count() == 0:
            id = 1
        else:
            id = Appointment.objects.order_by('-id').first().id + 1
        start_date = request.POST['start_date']
        start_hour = request.POST['start_hour']
        end_hour = request.POST['end_hour']
        doctor = request.user
        if request.POST['patient']:
            patient = User.objects.get(id=request.POST['patient'])
        else:
            patient = None
        print(patient)

        end_date = start_date + ' ' + end_hour + ':00'
        start_date = start_date + ' ' + start_hour + ':00'

        start_date = datetime.datetime.strptime(str(start_date), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

        new_appointment = Appointment(id=id, description='', start_date=start_date, end_date=end_date, date_reserved=None, doctor=doctor, patient=patient)
        new_appointment.save()

        print(start_date)
    elif request.method == 'POST' and "button-remove" in request.POST:
        appointment_id_to_remove = request.POST['selectappointments']
        appointment_to_remove = Appointment.objects.filter(id=appointment_id_to_remove)
        appointment_to_remove.delete()

    elif request.GET:
        appointments_arr = []
        if request.GET.get('doctor') == 'all':
            all_appointments = Appointment.objects.all()
        else:
            all_appointments = Appointment.objects.filter(doctor__icontains=request.GET.get('doctor'))
        
        for i in all_appointments:
            appointments_sub_arr = {}
            appointments_sub_arr['title'] = i.title
            start_date = datetime.datetime.strptime(str(i.start_date.date()), "%Y-%m-%dT%H::%M::%S").strftime("%Y-%m-%dT%H::%M::%S")
            end_date = datetime.datetime.strptime(str(i.end_date.date()), "%Y-%m-%dT%H::%M::%S").strftime("%Y-%m-%dT%H::%M::%S")
            appointments_sub_arr['start'] = start_date
            appointments_sub_arr['end'] = end_date
            appointments_arr.append(appointments_sub_arr)
        return HttpResponse(json.dumps(appointments_arr))
    
    context = {
        "appointments": all_appointments,
        "get_appointment_doctors": get_appointment_doctors,
        "form": form,
    }
    return render(request, 'doctorcalendar.html', context)



def countPatientsWithoutDuplicates(patients, patient):
    for i in patients:
        if i == patient:
            return False
    return True

@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def doctorpanel(request):
    appointments_arr = []
    if request.method == 'GET':
        #total_appointments
        total_appointments = Appointment.objects.filter(doctor=request.user).count()
        print("WSZYSTKIE: ", total_appointments)
        
        #total_today_appointments
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        try:
            total_today_appointments = Appointment.objects.filter(doctor=request.user, start_date__range=(today_min, today_max)).count()
        except:
            total_today_appointments = 0
        print("WSZYSTKIE DZISIAJ: ", total_today_appointments)

        #total_patients
        patients = []
        all_appointments = Appointment.objects.filter(doctor=request.user)
        for a in all_appointments:
            if countPatientsWithoutDuplicates(patients, a.patient) and a.patient != None:
                patients.append(a.patient)
        print(patients)
        total_patients = len(patients)

        #total_work_hours
        total_work = datetime.timedelta(hours=0, minutes=0)
        for a in all_appointments:
            total_work += a.end_date-a.start_date
        print(total_work)
        total_work_days = total_work.days

        seconds = total_work.seconds
        total_work_hours = seconds//3600
        total_work_minutes = (seconds//60)%60
    
    context = {
        "total_appointments": total_appointments,
        "total_today_appointments": total_today_appointments,
        "total_patients": total_patients,
        "total_work_days": total_work_days,
        "total_work_hours": total_work_hours,
        "total_work_minutes": total_work_minutes
    }
    return render(request, 'doctorpanel.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def doctoraccount(request):
    return render(request, 'doctoraccount.html')
