from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#2A9D8F] focus:ring-2 focus:ring-[#2A9D8F]/20 outline-none transition duration-200 text-[#264653]'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#2A9D8F] focus:ring-2 focus:ring-[#2A9D8F]/20 outline-none transition duration-200 text-[#264653]'}),
        }
