from django.urls import path, include
from . import views
from django.conf.urls import url


urlpatterns = [
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('userhome', views.userhome, name="userhome"),
    path('logout', views.logout, name="logout"),

    path('doctorhome', views.doctorhome, name="doctorhome"),
    path('doctortoday', views.doctortoday, name="doctortoday"),
    path('doctorcalendar', views.doctorcalendar, name="doctorcalendar"),
    path('doctorpanel', views.doctorpanel, name="doctormedpanel"),
    path('doctoraccount', views.doctoraccount, name="doctoraccount"),
]