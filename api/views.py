from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.clinics.models import Clinic , User
from apps.clinics.serializesrs import ClinicSerializer , DoctorSerializer
# Create your views here.


class ClinicListSet(ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer




class DoctorView(ModelViewSet):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return User.objects.filter(roles__role__name="DOCTOR").prefetch_related("doctor_profile", "roles__role")
