from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.conf.urls import url

from django.core import serializers

# Create your views here.
from .models import *
# from .forms import CreateUserForm
from .forms import AppointmentForm
from .forms import AppointmentNoteForm

from .decorators import unauthenticated_user, allowed_users, login_decorator

from .models import Appointment

from django.http import JsonResponse
import json

from django.http import HttpResponse
# + HTTP Response - xhtml12pdf
from django.template.loader import get_template
from xhtml2pdf import pisa

from .filters import UserFilter

from django.views.generic import DetailView

from django.utils import translation
from django.utils.formats import date_format


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
@login_decorator
def userhome(request):
    return render(request, 'userpanel.html')

def logout(request):
    auth.logout(request)
    return redirect('login')


# DOCTOR ---------------------------------------------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor', 'Patient'])
def userpanel(request):
    return render(request, 'userpanel.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def doctortoday(request):
    today = datetime.date.today().strftime("%d.%m.%Y")
    today_appointments = None
    if request.is_ajax and request.method == 'POST':
        idDoneAppointment = request.POST['id'].replace('button:', '')
        currentAppointment = Appointment.objects.get(id=idDoneAppointment)
        print(currentAppointment)
        if currentAppointment.done == '':
            print(currentAppointment.done)
            currentAppointment.done = 'btn-done'
            print(currentAppointment.done)
            currentAppointment.save()
        elif currentAppointment.done == 'btn-done':
            currentAppointment.done = ''
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
        return redirect('doctorcalendar')

        print("START+DATE", start_date)
    elif (request.method == 'POST' and "button-remove" in request.POST) or (request.method == 'POST' and request.is_ajax):
        print(request)
        appointment_id_to_remove = request.POST['selectappointments']
        appointment_to_remove = Appointment.objects.filter(id=appointment_id_to_remove)
        appointment_to_remove.delete()
    elif request.GET:
        print("SIEMANDERO:", request)
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
            appointments_sub_arr['description'] = i.description
            appointments_arr.append(appointments_sub_arr)
        return HttpResponse(json.dumps(appointments_arr))
    
    context = {
        "appointments": all_appointments,
        "get_appointment_doctors": get_appointment_doctors,
        "form": form,
    }
    return render(request, 'doctorcalendar.html', context)



def render_pdf_view(request):
    #variables to pdf
    date =  str(datetime.date.today().strftime("%d.%m.%Y"))
    doctorName = request.user.first_name + " " + request.user.last_name
    
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    try:
        today_appointments = Appointment.objects.filter(doctor=request.user, start_date__range=(today_min, today_max))
    except:
        today_appointments = None

    template_path = 'pdf.html'
    context = {
        'date': date,
        'user': doctorName,
        'appointments': today_appointments,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
       print("ERROR")
    return response

def countPatientsWithoutDuplicates(patients, patient):
    for i in patients:
        if i == patient:
            return False
    return True

@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def doctorpanel(request):
    appointments_arr = []
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

    #days in week
    current_day = datetime.date.today()
    weekday = current_day.isoweekday()

    start_week = current_day - datetime.timedelta(days=weekday)

    week = [start_week + datetime.timedelta(days=i+1) for i in range(7)]

    #appointments count each week day
    counterAppointmentsDay = []
    for i in week:
        countOfDay = Appointment.objects.filter(doctor=request.user, start_date__year=i.year, start_date__month=i.month, start_date__day=i.day).count()
        counterAppointmentsDay.append(countOfDay)
        print(i, " tego dnia ", countOfDay)
    print(counterAppointmentsDay)

    #ajax date to filename
    todayDate = datetime.date.today().strftime("%d%m%Y")

    context = {
        "total_appointments": total_appointments,
        "total_today_appointments": total_today_appointments,
        "total_patients": total_patients,
        "total_work_days": total_work_days,
        "total_work_hours": total_work_hours,
        "total_work_minutes": total_work_minutes,
        "week": week,
        "countEachDay": counterAppointmentsDay,
        "today": todayDate
    }
    return render(request, 'doctorpanel.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor', 'Patient'])
def settings(request):
    if request.method == 'POST' and "update-personal-data" in request.POST:
        print("SIEMA")

        current_user = request.user

        current_user_profile = None

        if UserProfile.objects.filter(user=request.user).exists():
            current_user_profile = UserProfile.objects.get(user=current_user)
            current_user_profile.phone = request.POST['phone']
            current_user_profile.save()
        else:
            current_user_profile = UserProfile.objects.create(user=current_user, phone=request.POST['phone'])
            current_user_profile.save()
        
        

        current_user.first_name = request.POST['first_name']
        current_user.last_name = request.POST['last_name']
        current_user.email = request.POST['username']

        current_user.save()

        messages.success(request, "Pomyślnie zmieniono dane!")
        return redirect('settings')

    elif request.method == 'POST' and "update-password" in request.POST:
        oldpassword = request.POST['oldpassword']
        current_user = request.user

        if current_user.check_password(oldpassword):
            newpassword1 = request.POST['newpassword1']
            newpassword2 = request.POST['newpassword2']
            if newpassword1 == newpassword2:
                current_user.set_password(newpassword1)
                current_user.save()
                messages.success(request, "Pomyślnie zmieniono hasło!")
                update_session_auth_hash(request, request.user)
                return redirect('settings')
            else:
                messages.error(request, "Nowe hasła nie są takie same!")
                return redirect('settings')
        else:
            messages.error(request, "Podane obecne hasło jest niepoprawne!")
            return redirect('settings')
    
    userPhone = UserProfile.objects.get(user=request.user).phone if UserProfile.objects.filter(user=request.user).exists() else ""

    context = {
        "user_phone": userPhone
    }
    return render(request, 'settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Doctor'])
def searchpatient(request):
    user_list = User.objects.filter(groups__name="Patient").order_by('last_name')
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'searchpatient.html', {'filter': user_filter})

def details(request, pk):
    request_patient = User.objects.get(id=pk)
    appointments_notes = AppointmentNote.objects.filter(patient=request_patient).order_by('-appointment__start_date')
    form = AppointmentNoteForm()
    all_appointments = Appointment.objects.filter(doctor=request.user, patient=request_patient).order_by('-start_date')
    if (request.method == 'POST' and "deleteappointmentnote" in request.POST):
        appointmentnote_id_to_remove = request.POST['deleteappointmentnote']
        appointmentnote_to_remove = AppointmentNote.objects.filter(id=appointmentnote_id_to_remove)
        appointmentnote_to_remove.delete()
        return redirect('details', pk=pk)
    elif (request.method == 'POST' and "edit-appointment_note" in request.POST):
        new_note = request.POST['edit-appointment_note']
        keys = list(request.POST.keys())
        id_note = str(keys[2])
        edit_appointmentnote = AppointmentNote.objects.get(id=id_note)
        edit_appointmentnote.note = new_note
        edit_appointmentnote.save()
        return redirect('details', pk=pk)
    elif request.method == 'POST' and 'selectappointmentnote' in request.POST:
        if AppointmentNote.objects.count() == 0:
            id = 1
        else:
            id = AppointmentNote.objects.order_by('-id').first().id + 1
        print(request.POST)
        current_appointment_id = request.POST['selectappointmentnote']
        current_appointment = Appointment.objects.get(id=current_appointment_id)
        note = request.POST['appointment_note']
        new_appointment_note = AppointmentNote(patient=request_patient, appointment=current_appointment, note=note)
        new_appointment_note.save()
        return redirect('details', pk=pk)
    context = {
        'patient': request_patient,
        'appointments_notes': appointments_notes,
        'form': form,
        'all_appintments': all_appointments,
    }
    return render(request, 'patientdetails.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Patient'])
def patientappointments(request):
    my_appointments = Appointment.objects.filter(patient=request.user).order_by('start_date')

    context = {
        'appointments': my_appointments,
    }
    return render(request, 'patientappointments.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['Patient'])
def booking(request):
    user_list = User.objects.filter(groups__name="Doctor").order_by('last_name')
    user_filter = UserFilter(request.GET, queryset=user_list)
    context = {
        'filter': user_filter
    }
    return render(request, 'patientbooking.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Patient'])
def doctorappointments(request, pk):
    inf_date = datetime.date(3000, 1, 1)

    two_weeks = []
    for i in range(15):
        translation.activate('pl')
        two_weeks.append((datetime.date.today() + datetime.timedelta(days=i)))
        

    today = datetime.date.today()
    doctor = User.objects.get(id=pk)
    all_appointments = Appointment.objects.filter(doctor=doctor, start_date__range=(today, inf_date)).order_by('start_date')


        
    context = {
        'appointments': all_appointments,
        'weeks': two_weeks,
        'doctor': doctor
    }
    return render(request, 'doctorappointments.html', context)