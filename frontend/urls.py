from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('clinics/', views.clinics_list, name='clinics_list'),
    path('clinics/<int:pk>/', views.clinic_detail, name='clinic_detail'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('services/', views.services_list, name='services_list'),
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('about/', views.about, name='about'),
]