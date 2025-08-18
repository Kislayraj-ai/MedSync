from .models import Clinic , DoctorProfile , UserRole , Roles
from django.contrib.auth.models import User
from rest_framework import serializers

class ClinicSerializer(serializers.ModelSerializer):

    class Meta :
        model =  Clinic
        fields =  "__all__"

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
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
    doctor_profile = DoctorProfileSerializer(many=True, read_only=True)
    roles = UserRoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "roles", "doctor_profile"]
