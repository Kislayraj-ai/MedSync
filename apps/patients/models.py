from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class PatientProfile(models.Model):

    class MaritialChoices(models.TextChoices):
        Single = "single", "Single"
        Married = "married", "Married"
        Divorced = "divorced", "Divorced"
        Widowed = "widowed", "Widowed"

    class SexChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"    

    # main info --
    patient =  models.ForeignKey(User , on_delete=models.CASCADE , related_name="patient_user")
    doctor =  models.ForeignKey(User , on_delete=models.CASCADE , related_name="patients_doctor")
    

    registration_datetime = models.DateTimeField(auto_now_add=True)
    
    # basic info ---
    healthcare_number = models.CharField(max_length=50, unique=True)  # eg: 23
    sex = models.CharField(
        max_length=10,
        choices=SexChoices.choices ,
        default=SexChoices.OTHER,
    )
    dob = models.DateField()
    p_age = models.IntegerField(null=False , blank=False)

    # addres --
    street_address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)



    #  other info --
    marital_status = models.CharField(
        max_length=20,
        choices=MaritialChoices.choices,
        default=MaritialChoices.Single ,
        blank=True,
        null=True,
    )

    # emergency Contact ---
    emergency_first_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_last_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_relationship = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)


    # health History ---
    reason_for_registration = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    # insurance --
    insurance_id = models.CharField(max_length=100, blank=True, null=True)

    profile_img = models.ImageField(upload_to='patient/patientImg' , blank=True, null=True )



    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} ({self.healthcare_number})"

    @property
    def age(self):
        today =  date.today()
        getage = today.year - self.dob.year

        if (today.month, today.day) < (self.dob.month, self.dob.day):
            getage -= 1

        return getage

    # @property
    # def save(self, *args, **kwargs):
    #     if self.dob:
    #         today = date.today()
    #         calculated_age = today.year - self.dob.year
    #         if (today.month, today.day) < (self.dob.month, self.dob.day):
    #             calculated_age -= 1
    #         self.age = calculated_age
    #     super().save(*args, **kwargs)
