from django.shortcuts import render , redirect , get_object_or_404 
from web_project  import TemplateLayout
from django.views.generic import TemplateView
from django.conf import settings
from .models import PatientProfile , Apointment
from django.contrib.auth.models import User
from datetime import date , datetime
from django.contrib import messages
from .forms import UserForm , PatientProfileForm
from django.db import transaction
from django.urls import reverse

# Create your views here.

class PatientAdd(TemplateView):

    def get_context_data(self , **kwargs):
        context = TemplateLayout.init(self , super().get_context_data(**kwargs))
        context["page_title"] = 'Add Patients'
        context["BASE_URL"] = settings.BASE_URL

        ## get from the query params
        date = self.request.GET.get("date")
        time = self.request.GET.get("time")
        clinicid = self.request.GET.get("clinicid")
        doctorid = self.request.GET.get("doctor")
        

        context["user_form"] = kwargs.get('user_form' , UserForm())
        context["profile_form"] = kwargs.get('profile_form' , PatientProfileForm)

        context["selecteddate"] = date
        context["selectedtime"] = time

        context["clinicid"] = clinicid
        context["doctorid"] = doctorid

        return context
    
   
    def post(self, request , *args, **kwargs):

        if request.method == "POST" :
            try:  
                if request.method == "POST": 
                    user_form = UserForm(request.POST)
                    profile_form =  PatientProfileForm(request.POST , request.FILES)
                    if user_form.is_valid() and profile_form.is_valid():
                        with transaction.atomic():
                            user = user_form.save(commit=False)
                            user.username = (request.POST.get('first_name', '') + request.POST.get('last_name', '')).lower()
                            

                            dob_str =  request.POST.get('dob')
                            dob = datetime.strptime(dob_str, "%Y-%m-%d").date() 

                            profile = profile_form.save(commit=False)
                            profile.patient = user
                            # profile.doctor_id = request.POST.get('doctor')

                            today = date.today()
                            calculated_age = today.year - dob.year
                            if (today.month, today.day) < (dob.month, dob.day):
                                calculated_age -= 1
                            
                            profile.p_age = calculated_age

                            ## save the appointment for the patient
                            doctorid = request.POST.get('doctor')
                            appdate = request.POST.get('appdate')
                            apptime = request.POST.get('apptime')
                            appdate_obj = datetime.strptime(appdate, "%Y-%m-%d").date()
                            apptime_obj = datetime.strptime(apptime, "%H:%M").time()

                            app =  Apointment()
                            app.doctor_id =  doctorid
                            app.patient = profile
                            app.appdate = appdate_obj
                            app.apptime = apptime_obj
                            app.status =  0
                            app.is_active =  0
                    
                            user.save()
                            profile.save()
                            app.save()

                        messages.success(request, "Patient created successfully")
                        return redirect("add_appointment")
                    else:
                        # print("UserForm Errors:", user_form.errors)
                        # print("ProfileForm Errors:", profile_form.errors)
                        messages.error(request, "There are some issues in the forms")

                        context = self.get_context_data(
                            user_form=user_form,
                            profile_form=profile_form
                        )
                        return self.render_to_response(context)

            except Exception as e :
                messages.error(request, f"Error :- {e}")
                return redirect("add_appointment")
            

class PatientEdit(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self , super().get_context_data(**kwargs))
        context["BASE_URL"] = settings.BASE_URL 
        context["Page_title"] = "Edit Patients"

        # pid =  self.kwargs.get('pk')
        appId = self.request.GET.get("appointment")

        ## fetch the patient data
        appointment = Apointment.objects.get(id=appId)
        
        patientprofile =  PatientProfile.objects.get(id=appointment.patient_id)

        patientdata = User.objects.get(pk=patientprofile.patient_id)


        user_form =  UserForm(instance=patientdata)
        profile_form = PatientProfileForm(instance=patientprofile)

        context["paientdata"] = patientdata
        context["patientprofile"] = patientprofile
        context["appointment"] = appointment

        context["user_form"] = user_form
        context["profile_form"] = profile_form

        return context


    def post(self, request , *args, **kwargs):

        # user_id
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, pk=user_id)

        appointment_id = request.POST.get("appointment_id")
        url =  reverse("patient_edit")
        query_string =  f"?appointment={appointment_id}"
        fullurl =  f"{url}{query_string}"
        
        profile = user.patient_user.first()

        if not user_id :
                messages.warning(request, "Valid Patient id is missing!!")
                return redirect(fullurl)

        if request.method == "POST" :
            # print(user)
            try:
                user_form =  UserForm(request.POST , instance=user)
                profile_form =  PatientProfileForm(request.POST , request.FILES , instance=profile)

                if user_form.is_valid() and profile_form.is_valid():

                    with transaction.atomic():

                        user =  user_form.save(commit=False)
                        user.username = (request.POST.get('first_name', '') + request.POST.get('last_name', '')).lower()

                        dob_str =  request.POST.get('dob')
                        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

                        profile_form.patient = user
                        profile_form.doctor_id = request.POST.get('doctor')

                        today =  date.today()
                        calculate_age  = today.year -  dob.year

                        if (dob.month , dob.day) < (today.month , today.day):
                            calculate_age -= 1

                        profile_form.age = calculate_age

                        #! save the appointment here
                        apptime = request.POST.get('apptime')
                        apptime_obj = datetime.strptime(apptime, "%H:%M").time()
                        app  = Apointment.objects.get(id=appointment_id)
                        # app.doctor_id =  doctorid
                        # app.patient = profile
                        # app.appdate = appdate_obj
                        app.apptime = apptime_obj
                        # app.status =  0
                        # app.is_active =  0


                        user.save()
                        profile_form.save()
                        app.save()

                        messages.success(request, "Patient updated successfully")
                        return redirect(fullurl)

            except Exception as e :
                    messages.error(request, f"Error:- {e}")
                    return redirect(fullurl)
            

## add the appointment
class AddAppointmentView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self , super().get_context_data(**kwargs))
        context["page_title"] = 'Add Appointment' 
        return context
    


 # def post(self, request , *args, **kwargs):
    #         if request.method == "POST":
    #             try:
    #                 # Patient basic info
    #                 profile_image = request.FILES.get("profile_image")
    #                 first_name = request.POST.get("first_name")
    #                 last_name = request.POST.get("last_name")
    #                 email = request.POST.get("email")
    #                 # phone = request.POST.get("phone")
    #                 doctor = request.POST.get("doctor")
    #                 healthcare_number = request.POST.get("healthcare_number")
    #                 sex = request.POST.get("sex")
    #                 dob = request.POST.get("dob")

    #                 # Address
    #                 street_address = request.POST.get("street_address")
    #                 city = request.POST.get("city")
    #                 state = request.POST.get("state")
    #                 country = request.POST.get("country")
    #                 postal_code = request.POST.get("postal_code")

    #                 # Marital status
    #                 marital_status = request.POST.get("marital_status")

    #                 # Emergency contact
    #                 emergency_first_name = request.POST.get("emergency_first_name")
    #                 emergency_last_name = request.POST.get("emergency_last_name")
    #                 emergency_relationship = request.POST.get("emergency_relationship")
    #                 emergency_contact_number = request.POST.get("emergency_contact_number")

    #                 # Insurance
    #                 insurance_id = request.POST.get("insurance_id")


    #                 if not first_name or not last_name  or not dob or not country or not doctor :
    #                     messages.warning(request , "Some required filed cannot be empty")
    #                     return redirect('add_appointment')

    #                 user =  User()
    #                 user.username =  first_name +" " + last_name
    #                 user.first_name =  first_name
    #                 user.last_name =  last_name
    #                 user.email =  email

    #                 user.save()

    #                 # now the patient profile
    #                 patientProfile = PatientProfile()
    #                 patientProfile.profile_img = profile_image
                    
    #                 patientProfile.patient = user
    #                 patientProfile.doctor =  User.objects.get(id=doctor)
    #                 patientProfile.registration_datetime =  datetime.now().strftime("%Y-%m-%d")
    #                 patientProfile.healthcare_number =  healthcare_number
    #                 patientProfile.sex =  sex
    #                 patientProfile.dob =  dob

    #                 patientProfile.country =  country
    #                 patientProfile.state =  state
    #                 patientProfile.city =  city
    #                 patientProfile.street_address =  street_address
    #                 patientProfile.postal_code =  postal_code

    #                 patientProfile.marital_status =  marital_status
    #                 patientProfile.emergency_first_name  = emergency_first_name
    #                 patientProfile.emergency_last_name  = emergency_last_name
    #                 patientProfile.emergency_relationship  = emergency_relationship
    #                 patientProfile.emergency_contact_number  = emergency_contact_number
    #                 patientProfile.insurance_id = insurance_id

    #                 patientProfile.save()

    #                 ## save message to the server
    #                 messages.success(request , 'Patient save successfully !!')
    #                 return redirect('add_appointment')
                
    #             except Exception as e :
    #                 messages.error(request , f"Error :- {e}")
    #                 return redirect('add_appointment')
