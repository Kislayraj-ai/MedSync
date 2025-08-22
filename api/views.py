from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.clinics.models import Clinic , User
from apps.clinics.serializesrs import ClinicSerializer , DoctorSerializer ,PatientSerializer
from rest_framework import generics
from apps.patients.models  import PatientProfile
# Create your views here.


class ClinicListSet(ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer




class DoctorView(ModelViewSet):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return User.objects.filter(roles__role__name="DOCTOR").prefetch_related("doctor_profile", "roles__role")


## for patients

class PatientListView(generics.ListAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class =  PatientSerializer

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)