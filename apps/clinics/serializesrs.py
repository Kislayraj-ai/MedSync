from .models import Clinic , DoctorProfile , UserRole , Roles , ClinicTime , AdminUserProfile
from django.contrib.auth.models import User
from rest_framework import serializers
from apps.patients.models import PatientProfile , Apointment , PaymentHistory
from django.contrib.auth.models import User

class ClinicSerializer(serializers.ModelSerializer):

    class Meta :
        model =  Clinic
        fields =  "__all__"

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = "__all__"

class ClinicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUserProfile
        fields = "__all__"

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ["id", "name"]

class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = UserRole
        fields = ["role"]


class DoctorSerializer(serializers.ModelSerializer):
    doctor_profile = DoctorProfileSerializer(read_only=True)
    roles = UserRoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "roles", "doctor_profile"]


class ClinicUserSerializer(serializers.ModelSerializer):
    
    roles = UserRoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "roles"]

## for the patient

# serializers.py
class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['id', 'amount', 'appDate', 'appTime', 'status', 'appointment_id']


class AppointmentSerializer(serializers.ModelSerializer):
    payment_appointment = PaymentHistorySerializer(read_only=True)

    doctorfullname =  serializers.SerializerMethodField()
    patientFullname =  serializers.SerializerMethodField()

    def get_doctorfullname(self, obj):
        return f"{obj.doctor.first_name} {obj.doctor.last_name}"
    
    def get_patientFullname(self, obj):
        return f"{obj.patient.patient.first_name} {obj.patient.patient.last_name}"

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    active_status_display = serializers.CharField(source='get_is_active_display', read_only=True)


    class Meta:
        model = Apointment
        fields = ['id', 'appdate', 'apptime', 'status',
                'is_active', 'created_at', 'doctor_id',
                'patient_id','patientFullname' , 'payment_appointment' , 'doctorfullname' , 'status_display' , 'active_status_display']


class PatientSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(source="patient.id", read_only=True)
    username = serializers.CharField(source="patient.username", read_only=True)
    firstname = serializers.CharField(source="patient.first_name", read_only=True)
    lastname = serializers.CharField(source="patient.last_name", read_only=True)
    email = serializers.CharField(source="patient.email", read_only=True)

    # doctorfullname =  serializers.SerializerMethodField()

    # def get_doctorfullname(self, obj):
    #     return f"{obj.doctor.first_name} {obj.doctor.last_name}"

    appointment_patient =  AppointmentSerializer(many=True , read_only=True)
    
    class Meta :
        model = PatientProfile

        fields =  [f.name for f in PatientProfile._meta.fields] + [
            "userid" ,
                "username",
                "email",
                "firstname",
                "lastname",
                # "doctorfullname",
                "appointment_patient"
        ]

class ClinicTimeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicTime
        fields =  '__all__'
