from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment, Doctor


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('doctor_list')
    else:
        form = UserCreationForm()
    return render(request, 'clinic/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('doctor_list')
    else:
        form = AuthenticationForm()
    return render(request, 'clinic/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinic/doctor_list.html', {'doctors': doctors})

@login_required 
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'clinic/my_appointments.html', {'appointments': appointments})

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.patient = request.user
                appointment.doctor = doctor
                appointment.save()
                messages.success(request, 'Appointment booked successfully.')
                return redirect('my_appointments')
            except IntegrityError:
                messages.error(request, 'This time slot is already booked. Please choose another.')
    else:
        form = AppointmentForm()
    return render(request, 'clinic/book_appointment.html', {'form': form, 'doctor': doctor})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    if request.method == 'POST':
        appointment.delete()
        return redirect('my_appointments')
    return render(request, 'clinic/cancel_appointment.html', {'appointment': appointment})