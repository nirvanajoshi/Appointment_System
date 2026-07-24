from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.doctor_list, name='doctor_list'),
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('appointments/book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]