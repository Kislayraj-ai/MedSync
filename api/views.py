from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.clinics.models import Clinic , User , ClinicTime , DoctorProfile , AdminUserProfile 
from apps.clinics.serializesrs import ClinicSerializer , DoctorSerializer ,PatientSerializer ,\
    ClinicTimeSlotsSerializer , AppointmentSerializer , ClinicUserSerializer
from rest_framework import generics , status
from apps.patients.models  import PatientProfile, Apointment
from rest_framework.response import Response
from datetime import timedelta , datetime
from rest_framework.views import APIView
from django.conf import settings
from requests.auth import HTTPBasicAuth
import requests
import json
import uuid
from .utility import get_user_clinic_ids
from rest_framework.permissions import AllowAny  , IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


class ClinicListSet(ModelViewSet):
    serializer_class = ClinicSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        curruser = self.request.user
        clinic_ids = []

        if curruser.is_superuser:
            return Clinic.objects.all()

        else:
            clinic_ids = get_user_clinic_ids(curruser , AdminUserProfile , DoctorProfile)

        return Clinic.objects.filter(id__in=clinic_ids)


class ClinicAdminUsers(generics.ListAPIView):
    serializer_class = ClinicUserSerializer

    def get_queryset(self):

        qs = User.objects.all()
        curruser = self.request.user
        getid = self.request.GET.get('clinicid')

        if not curruser.is_superuser :
            clinic_ids = get_user_clinic_ids(curruser , AdminUserProfile , DoctorProfile)
            if clinic_ids is not None:
                qs = qs.filter(
                    Q(doctor_profile__clinic_id__in=clinic_ids) |
                    Q(admin_profile__clinic_id__in=clinic_ids)
                )

        qs = (  
            qs.filter(roles__role__name__in=["ADMIN" , "DOCTOR"] )
            .prefetch_related("roles__role")
        )

        if getid is not None:
            qs = qs.filter(doctor_profile__clinic_id=getid)

        return qs


class DoctorView(ModelViewSet):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        getid = self.request.GET.get('clinicid')
        alldoctors = (
            User.objects.filter(roles__role__name="DOCTOR")
            .select_related("doctor_profile")
            .prefetch_related("roles__role")
        )

        if getid is not None:
            alldoctors = alldoctors.filter(doctor_profile__clinic_id=getid)

        return alldoctors




## for patients

class PatientListView(generics.ListAPIView):
    # queryset = PatientProfile.objects.all()
    serializer_class =  PatientSerializer
    
    def get_queryset(self):
        qs = PatientProfile.objects.all()
        curruser = self.request.user

        # get clinic IDs for current user
        clinic_ids = get_user_clinic_ids(curruser , AdminUserProfile , DoctorProfile)
        if clinic_ids is not None:
            qs = qs.filter(
                appointment_patient__doctor__doctor_profile__clinic_id__in=clinic_ids
            )

        # apply filters
        start = self.request.GET.get("start")
        end = self.request.GET.get("end")
        clinicid = int(self.request.GET.get("clinicid", 0) or 0)

        if start and end:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
            qs = qs.filter(
                appointment_patient__appdate__range=[start_dt.date(), end_dt.date()]
            )

        if clinicid > 0:
            qs = qs.filter(
                appointment_patient__doctor__doctor_profile__clinic_id=clinicid
            )

        return qs.distinct()


class ClinicAvailableTimeSlots(generics.ListAPIView):

    serializer_class = None  

    def list(self, request, *args, **kwargs):
        clinicid = request.GET.get('clinicid') or request.data.get('clinicid')
        doctor = request.GET.get('doctorid') or request.data.get('doctorid')
        date = request.GET.get('date') or request.data.get('date')
        apptime = request.GET.get('apptime') or request.data.get('apptime')


        date_obj =  datetime.strptime(date , '%Y-%m-%d').date()
        getdayint =  date_obj.weekday()

        # apptime_obj =  None
        # if apptime:
        #     apptime_obj =  datetime.strptime(apptime , '%H:%M')

        if not clinicid or not date :
            return Response({
                "error": "clinicid and date are required" ,
                "status": status.HTTP_400_BAD_REQUEST
                });
    
        try:
            getuser =  User.objects.prefetch_related('doctor_profile').get(id=doctor)
            getdoctor =  getuser.doctor_profile
            
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


        booked =  Apointment.objects.filter(
            doctor = getuser ,
            appdate = date_obj ,
            status__in = [0 , 3]
        ).values_list('apptime' , flat=True)

        booked =  [t.strftime("%H:%M") for t in booked]

        available_slots = [s for s in slots if s not in booked ]

        # print("Getheap available sltos " , apptime_obj.strftime("%H:%M"))
        # if apptime_obj is not None :
        #     available_slots.append(apptime_obj.strftime("%H:%M"))

        available_slots.sort()

        return Response({
            'status' : status.HTTP_200_OK ,
            'clinic' :  clinicid ,
            'datestr' : date ,
            'available' : available_slots ,
            # 'doctor_clinic' : getuser.id,
            'booked' : booked 
        })
    

class GetAppointmentView(generics.ListAPIView):
    # queryset = Apointment.objects.all()
    queryset =  None
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        curruser = self.request.user
        appoinment = self.request.GET.get('appointment' , 0)
        clinic_ids = []

        if curruser.is_superuser:
            queryset = Apointment.objects.all()
        else:
            user_role = curruser.roles.first()
            if user_role and user_role.role.id == 1:
                clinic_ids = AdminUserProfile.objects.filter(user=curruser).values_list("clinic_id", flat=True)
            else:
                clinic_ids = DoctorProfile.objects.filter(user=curruser).values_list("clinic_id", flat=True)

            queryset = Apointment.objects.filter(doctor__doctor_profile__clinic_id__in=clinic_ids)

        if int(appoinment) > 0:
            queryset =  queryset.filter(id=appoinment)
        
        return queryset
    
class CancelAppointmentView(generics.UpdateAPIView):
    queryset =  Apointment.objects.all()
    serializer_class =  AppointmentSerializer
    lookup_field = 'id'
    

    def patch(self, request, *args, **kwargs):
        appointment_id = request.GET.get('id')
        # print("Getsdkpds " , appointment_id)
        if not appointment_id:
            return Response({"error": "Appointment ID required"}, status=400)

        try:
            appointment = Apointment.objects.get(id=appointment_id)
        except Apointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(appointment, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK  )


# paypal integration

class CreatePaypalOrderView(APIView):
    def post(self, request):
        amount = request.data.get("amount")
        appointment = request.data.get("appointment")

        if not amount or not appointment:
            return Response({"error": "Amount and appointment are required"}, status=400)
        
        # print(f"IDHAR AMOUt {amount} {appointment} ")

        token_res = requests.post(
            f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=HTTPBasicAuth(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
            data={"grant_type": "client_credentials"}
        )

        access_token = token_res.json().get("access_token")
        # access_token = ''

        payload = {
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {
                        "currency_code": "USD", "value": str(amount) ,

                        
                        },
                        "custom_id": str(appointment)
                }],
                "application_context": {
                    "return_url": f"{settings.BASE_URL}/patients/paypal/success-payment/",
                    "cancel_url": f"{settings.BASE_URL}/patients/paypal/cancel-payment/"
                }
            }


        headers = {
                "Content-Type": "application/json", 
                "PayPal-Request-Id": str(uuid.uuid4()) ,
                "Authorization": f"Bearer {access_token}"}
        
        res = requests.post(
            f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders",
            headers=headers,
            # json=payload
            json=payload
        )

        # print("===== RAW REQUEST PAYLOAD =====")
        # print(json.dumps(payload, indent=4))
        # print("===== RAW RESPONSE =====")
        # print(res.status_code, res.text)



        approval_url = None
        for link in res.json().get("links", []):
            if link["rel"] == "approve":
                approval_url = link["href"]

        return Response({"approval_url": approval_url})
