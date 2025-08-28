from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.clinics.models import Clinic , User , ClinicTime , DoctorProfile
from apps.clinics.serializesrs import ClinicSerializer , DoctorSerializer ,PatientSerializer , ClinicTimeSlotsSerializer
from rest_framework import generics
from apps.patients.models  import PatientProfile, Apointment
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta , datetime
# Create your views here.


class ClinicListSet(ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer




class DoctorView(ModelViewSet):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        getid = self.request.GET.get('clinicid')
        alldoctors = User.objects.filter(roles__role__name="DOCTOR").prefetch_related("doctor_profile", "roles__role")

        if getid is not None:
            alldoctors = alldoctors.filter(doctor_profile__clinic_id=getid)

        return alldoctors


## for patients

class PatientListView(generics.ListAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class =  PatientSerializer

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)


class ClinicAvailableTimeSlots(generics.ListAPIView):
    # queryset =  ClinicTime.objects.all()
    # serializer_class =  ClinicTimeSlotsSerializer
    serializer_class = None  

    def list(self, request, *args, **kwargs):
        clinicid =  request.GET.get('clinicid')
        date =  request.GET.get('date')
        time =  request.GET.get('time')
        doctor = request.GET.get('doctorid')

        date_obj =  datetime.strptime(date , '%Y-%m-%d').date()
        getdayint =  date_obj.weekday()

        if not clinicid or not date :
            return Response({
                "error": "clinicid and date are required" ,
                "status": status.HTTP_400_BAD_REQUEST
                });
    
        try:
            getuser =  User.objects.get(id=doctor)
            getdoctor =  DoctorProfile.objects.get(user=getuser)
            
            if getdoctor.clinic_id != int(clinicid):
                return Response({
                    "error": "Doctor not present in clinic" ,
                    "status": status.HTTP_404_NOT_FOUND
                });


        except User.DoesNotExist :
            return Response({
                            "error": "Clinic time does not exists",
                            "status": status.HTTP_404_NOT_FOUND,
                            "test": available_slots,
                            "clinic": getdayint
                        })
    
        try:
            clinic_time =  ClinicTime.objects.get(clinic_id=clinicid , day=getdayint)

        except ClinicTime.DoesNotExist  as e :
            return Response({
                'error' : 'Clinic time does not exists' ,
                'status' : status.HTTP_404_NOT_FOUND 
            })

            
        start_time =  clinic_time.open_time
        end_time =  clinic_time.end_time
        slotduration =  timedelta(minutes=30)

        
        slots = []

        current     =  datetime.combine(date_obj , start_time)
        enddatetime =  datetime.combine(date_obj , end_time)


        while current < enddatetime :
            slots.append(current.strftime("%H:%M"))
            current += slotduration

        ## get all the doctors for the particular clinic
        # doctor_clinic =  DoctorProfile.objects.filter(clinic_id=clinicid).values_list('id' , flat=True)
        # doctor_clinic = list(doctor_clinic)

        booked =  Apointment.objects.filter(
            doctor = getuser ,
            appdate = date_obj
        ).values_list('apptime' , flat=True)

        booked =  [t.strftime("%H:%M") for t in booked]
        # if s not in booked
        available_slots = [s for s in slots if s not in booked ]


        return Response({
            'status' : status.HTTP_200_OK ,
            'clinic' :  clinicid ,
            'datestr' : date ,
            'available' : available_slots ,
            # 'doctor_clinic' : getuser.id,
            'booked' : booked 
        })