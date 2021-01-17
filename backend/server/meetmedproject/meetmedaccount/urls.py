from django.urls import path, include
from . import views
from django.conf.urls import url


urlpatterns = [
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('userhome', views.userhome, name="userhome"),
    path('logout', views.logout, name="logout"),

    path('userpanel', views.userpanel, name="userpanel"),
    path('doctortoday', views.doctortoday, name="doctortoday"),
    path('doctorcalendar', views.doctorcalendar, name="doctorcalendar"),
    path('doctorpanel', views.doctorpanel, name="doctorpanel"),
    path('render_pdf_view', views.render_pdf_view, name="render_pdf_view"),
    
    path('patientappointments', views.patientappointments, name='patientappointments'),
    path('booking', views.booking, name="booking"),
    path('doctor/<int:pk>', views.doctorappointments, name='doctor'),

    url(r'^searchpatient/$', views.searchpatient, name='searchpatient'),
    path('settings', views.settings, name="settings"),
    path('details/<int:pk>', views.details, name='details')
]