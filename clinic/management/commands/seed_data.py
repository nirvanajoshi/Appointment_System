from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clinic.models import Doctor, Appointment
from datetime import date, time, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seeds the database with dummy data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))

        # ──────── Create Doctors ────────
        doctors_data = [
            {'name': 'Arun Sharma', 'specialty': 'Cardiology'},
            {'name': 'Priya Mehta', 'specialty': 'Dermatology'},
            {'name': 'Rohan Desai', 'specialty': 'Pediatrics'},
            {'name': 'Sneha Patel', 'specialty': 'Orthopedics'},
            {'name': 'Vikram Singh', 'specialty': 'Neurology'},
            {'name': 'Anita Verma', 'specialty': 'Ophthalmology'},
        ]

        created_doctors = []
        for doc in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                name=doc['name'],
                defaults={'specialty': doc['specialty']}
            )
            if created:
                self.stdout.write(f"  [CREATED] Dr. {doctor.name} ({doctor.specialty})")
            else:
                self.stdout.write(f"  [EXISTS] Dr. {doctor.name}")
            created_doctors.append(doctor)

        # ──────── Create User ────────
        username = 'Damodar_Joshi'
        password = 'demo12345'

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': 'damodar.joshi@example.com'}
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(f"  [CREATED] User: {username}")
        else:
            user.set_password(password)
            user.save()
            self.stdout.write(f"  [EXISTS] User: {username} (password reset)")

        # ──────── Create Appointments ────────
        today = timezone.localdate()

        appointments_data = [
            {
                'doctor': created_doctors[0],
                'patient': user,
                'date': today + timedelta(days=1),
                'time': time(9, 0),
                'status': 'scheduled',
            },
            {
                'doctor': created_doctors[1],
                'patient': user,
                'date': today + timedelta(days=2),
                'time': time(14, 30),
                'status': 'confirmed',
            },
            {
                'doctor': created_doctors[2],
                'patient': user,
                'date': today - timedelta(days=1),
                'time': time(11, 0),
                'status': 'cancelled',
            },
            {
                'doctor': created_doctors[3],
                'patient': user,
                'date': today + timedelta(days=5),
                'time': time(10, 0),
                'status': 'scheduled',
            },
            {
                'doctor': created_doctors[4],
                'patient': user,
                'date': today + timedelta(days=7),
                'time': time(15, 0),
                'status': 'confirmed',
            },
        ]

        for apt in appointments_data:
            # Use get_or_create to avoid duplicates on re-run
            appointment, created = Appointment.objects.get_or_create(
                doctor=apt['doctor'],
                patient=apt['patient'],
                date=apt['date'],
                time=apt['time'],
                defaults={'status': apt['status']}
            )
            if created:
                self.stdout.write(
                    f"  [CREATED] Dr. {appointment.doctor.name} "
                    f"on {appointment.date} at {appointment.time} ({appointment.status})"
                )
            else:
                self.stdout.write(
                    f"  [EXISTS] Dr. {appointment.doctor.name} "
                    f"on {appointment.date} at {appointment.time}"
                )

        self.stdout.write(self.style.SUCCESS('\n=== Database seeding complete! ==='))
        self.stdout.write(f'   User: {username} / {password}')
        self.stdout.write(f'   Doctors: {Doctor.objects.count()}')
        self.stdout.write(f'   Appointments: {Appointment.objects.filter(patient=user).count()}')
