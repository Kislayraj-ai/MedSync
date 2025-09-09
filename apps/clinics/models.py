from django.db import models
from django.contrib.auth.models import User , AbstractUser
from datetime import time
from django.conf import settings
# Create your models here.

class Clinic(models.Model) :

    name = models.CharField(max_length=255 , null=False , blank=False)
    clinicid = models.CharField(max_length=255 , null=False , blank=False)
    phone =  models.CharField(max_length=15 , null=True)
    email =  models.EmailField(max_length=254  , null=False , blank=False)
    logo =  models.ImageField(upload_to='cliniclogo', default='')
    created_at =  models.DateTimeField(auto_now_add=True)
    is_active =  models.BooleanField(default=True)

    def _str__(self):
        return self.name
    
    class Meta:
        ordering = ['created_at']


class ClinicTime(models.Model):

    class DayChoices(models.IntegerChoices):
            MONDAY = 0, "Monday"
            TUESDAY = 1, "Tuesday"
            WEDNESDAY = 2, "Wednesday"
            THURSDAY = 3, "Thursday"
            FRIDAY = 4, "Friday"
            SATURDAY = 5, "Saturday"
            SUNDAY = 6, "Sunday"

    clinic = models.ForeignKey(Clinic ,  on_delete=models.CASCADE ,related_name='clinic_times')
    day = models.IntegerField( choices = DayChoices.choices  , null=True)
    open_time = models.TimeField(default=time(0, 0))   # 00:00 default
    end_time = models.TimeField(default=time(0, 0))
    is_closed =  models.BooleanField(default=False)


    def __str__(self):
        return f"{self.clinic.name } - {self.clinic.day}"



class Roles(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        DOCTOR = "DOCTOR", "Doctor"
        PATIENT = "PATIENT", "Patient"

    name = models.CharField(max_length=20, choices=RoleChoices.choices, unique=True)

    def __str__(self):
        return self.get_name_display()


## make the role for
class UserRole(models.Model):

    user = models.ForeignKey(User   , on_delete=models.CASCADE, related_name='roles')
    role =  models.ForeignKey(Roles , on_delete=models.CASCADE, related_name='users')

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['user' ,'role'] , name='unique_user_role' )
        ]

    def __str__(self):
        return F"{self.username} ({self.role})"
    
class DoctorProfile(models.Model):
    user  =  models.OneToOneField(User ,  on_delete=models.CASCADE , related_name="doctor_profile")
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    fees = models.DecimalField(max_digits=8, decimal_places=2 , null=True , blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"
    

class AdminUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="admins")
    # designation = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Admin {self.user.get_full_name()} - {self.clinic.name}"