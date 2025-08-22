## make user and profile form too 

from django import forms
from django.contrib.auth.models import User
from .models import PatientProfile

class UserForm(forms.ModelForm):
    class Meta :
        model =  User
        fields = ['first_name'  , 'last_name' , 'email']
        widgets = {
            "first_name" : forms.TextInput(attrs={"class" : "form-control"}) ,
            "last_name" : forms.TextInput(attrs={"class" : "form-control"}),
            "email" : forms.EmailInput(attrs={"class" : "form-control"})
            
        }

class PatientProfileForm(forms.ModelForm):

    class Meta :
        model =  PatientProfile
        exclude = ['patient' , 'doctor' , 'p_age']
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            # "doctor": forms.Select(attrs={"class": "form-control"}),
            "p_age": forms.Select(attrs={"class": "form-control"}),
            "profile_img": forms.FileInput(attrs={"class": "d-none", "id": "profile_image", "accept": "image/*"}),
            "healthcare_number": forms.TextInput(attrs={"class": "form-control"}),
            "sex": forms.Select(attrs={"class": "form-control"}),
            "street_address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
            "marital_status": forms.Select(attrs={"class": "form-control"}),
            "emergency_first_name": forms.TextInput(attrs={"class": "form-control"}),
            "emergency_last_name": forms.TextInput(attrs={"class": "form-control"}),
            "emergency_relationship": forms.TextInput(attrs={"class": "form-control"}),
            "emergency_contact_number": forms.TextInput(attrs={"class": "form-control"}),
            "insurance_id": forms.TextInput(attrs={"class": "form-control"}),
            "reason_for_registration": forms.Textarea(attrs={"class": "form-control" ,  "rows" : 3}),
            "additional_notes": forms.Textarea(attrs={"class": "form-control" , "rows" : 3}),
        }

        
