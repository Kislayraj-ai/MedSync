from django.shortcuts import render , redirect , get_object_or_404 
from web_project  import TemplateLayout
from django.views.generic import TemplateView
from django.conf import settings
from .models import PatientProfile , Apointment , PaymentHistory
from django.contrib.auth.models import User
from datetime import date , datetime
from django.contrib import messages
from .forms import UserForm , PatientProfileForm
from django.db import transaction
from django.urls import reverse
import requests
import traceback

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

        patient = int(self.request.GET.get("patient" , 0) or 0)


        if patient > 0:
            patientdata =  User.objects.prefetch_related('patient_user').get(id=patient) ;
            patientprofile =  patientdata.patient_user ;

            user_form =  UserForm(instance=patientdata)
            profile_form = PatientProfileForm(instance=patientprofile)

            context["user_form"] = user_form
            context["profile_form"] = profile_form
            context["readmitpatients"] = patient

        else:
            context["user_form"] = kwargs.get('user_form' , UserForm())
            context["profile_form"] = kwargs.get('profile_form' , PatientProfileForm())
            context["readmitpatients"] = patient


        context["selecteddate"] = date
        context["selectedtime"] = time

        context["clinicid"] = clinicid
        context["doctorid"] = doctorid

        return context
    

    def post(self, request , *args, **kwargs):

        if request.method == "POST" :
            try:  
                if request.method == "POST": 
                    
                    readmitpatient =  int(request.POST.get('readmitpatient' , 0) or 0)

                    if readmitpatient > 0 :
                        userdata = User.objects.prefetch_related('patient_user').get(id=readmitpatient)
                        patientProfile = userdata.patient_user

                        user_form = UserForm(request.POST , instance=userdata)
                        profile_form =  PatientProfileForm(request.POST , request.FILES ,  instance=patientProfile)

                    else:
                        user_form = UserForm(request.POST)
                        profile_form =  PatientProfileForm(request.POST , request.FILES)


                    if user_form.is_valid() and profile_form.is_valid():
                        
                        with transaction.atomic():
                            user = user_form.save(commit=False)

                            if user._state.adding:
                                user.username = (
                                    request.POST.get("first_name", "") + request.POST.get("last_name", "")
                                ).lower()
                                

                            user.save()

                            dob_str =  request.POST.get('dob')
                            dob = datetime.strptime(dob_str, "%Y-%m-%d").date() 

                            profile = profile_form.save(commit=False)

                            if profile._state.adding:
                                profile.patient = user
                                profile.healthcare_number = request.POST.get('healthcare_number')

                            today = date.today()
                            calculated_age = today.year - dob.year
                            if (today.month, today.day) < (dob.month, dob.day):
                                calculated_age -= 1
                            
                            profile.p_age = calculated_age
                            profile.save()

                            ## save the appointment for the patient
                            doctorid = request.POST.get('doctor')
                            appdate = request.POST.get('appdate')
                            apptime = request.POST.get('apptime')
                            appdate_obj = datetime.strptime(appdate, "%Y-%m-%d").date()
                            apptime_obj = datetime.strptime(apptime, "%H:%M").time()

                            ## get doctor
                            docInfo =  User.objects.prefetch_related('doctor_profile').get(id=doctorid)
                            doctor_profile = docInfo.doctor_profile

                            app =  Apointment()
                            app.doctor_id =  doctorid
                            app.patient = profile
                            app.appdate = appdate_obj
                            app.apptime = apptime_obj
                            app.status =  0
                            app.is_active =  0
                            app.save()

                            app.save()

                            # add patients here
                            payment =  PaymentHistory()
                            payment.appointment = app
                            # payment.patient = user
                            payment.amount = doctor_profile.fees
                            payment.appDate = appdate_obj
                            payment.appTime = apptime_obj
                            
                            
                            
                            payment.save()
                        

                        messages.success(request, "Patient created successfully")

                        url = reverse('complete_payment')
                        fullurl = f"{url}?appointment={app.id}"
                        return redirect(fullurl)

                    else:
                        print("UserForm Errors:", user_form.errors)
                        print("ProfileForm Errors:", profile_form.errors)
                        messages.error(request, "There are some issues in the forms")

                        context = self.get_context_data(
                            user_form=user_form,
                            profile_form=profile_form
                        )
                        return self.render_to_response(context)

            except Exception as e :
                messages.error(request, f"Error :- {e}")
                return redirect("add_patient")
            

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
        
        profile = user.patient_user

        if not user_id :
                messages.warning(request, "Valid Patient id is missing!!")
                return redirect(fullurl)

        if request.method == "POST" :

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


class PatientDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        try:
            context = TemplateLayout.init(self , super().get_context_data(**kwargs))
            context["page_title"] = 'Patient Detail' 

            pk = self.kwargs.get('pk')

            if pk is None:
                messages.error(self.request, 'Please provide correct id')
                return redirect('patient_list')


            userDetail = (
                User.objects
                .select_related("patient_user")   # safe now, OneToOneField hai
                .prefetch_related("patient_user__appointment_patient__payment_appointment")
                .get(pk=pk)
            )
            patientProfile =  userDetail.patient_user
            appointments = patientProfile.appointment_patient.all()
            
            appointment_data = [
                {
                    "appointment_id": app.id,
                    "date": app.appdate,
                    "doctor": app.doctor,
                    "is_active": app.get_is_active_display() ,
                    "payment": getattr(app, 'payment_appointment', None)
                }
                for app in appointments
            ]


            context["user_detail"] = userDetail
            context["patient_profile"] = patientProfile
            context["appointments"] = appointment_data

            # print(context["appointments"] )
            return context
        except Exception as e :
            # print(traceback.format_exc(e))
            print(e)

        

## add the appointment
class AddAppointmentView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self , super().get_context_data(**kwargs))
        context["page_title"] = 'Add Appointment' 
        return context
    

class CompletePaymentView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self , super().get_context_data(**kwargs))
        context["BASE_URL"] = settings.BASE_URL 
        context["page_title"] = 'Complete Payment' 

        appointment =  self.request.GET.get('appointment')
        context['appointment_id'] = appointment

        return context


def get_paypal_access_token():
    url = f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET)
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data, auth=auth)
    response.raise_for_status()
    return response.json()["access_token"]

class SuccessPaymentView(TemplateView):
    template_name = "patients/success.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["BASE_URL"] = settings.BASE_URL
        context["page_title"] = "Success Payment"

        token = self.request.GET.get("token")
        payer_id = self.request.GET.get("PayerID")

        print(f"YES HIT HUA IDHAR ======================== {token}")
        import json

        if token:
            try:
                capture_url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders/{token}/capture"
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {get_paypal_access_token()}"}
                response = requests.post(capture_url, headers=headers)
                order_data = response.json()

                # print("===== RAW CAPTURE DATA =====")
                # print(json.dumps(order_data, indent=4))

                if order_data.get("status") == "COMPLETED":
                    appointment_id = order_data["purchase_units"][0]["payments"]["captures"][0]["custom_id"]
                    # print(f"Captured appointment {appointment_id}")

                    
                    appointment_id =  int(appointment_id)
                    appointment = Apointment.objects.get(id=int(appointment_id))
                    payment = PaymentHistory.objects.get(appointment=appointment)
                    payment.status = "1"
                    payment.save()

                    appointment.status = "1"
                    appointment.save()

                    context["payment_success"] = True
                    context["appointment_id"] = appointment_id
                else:
                    context["payment_success"] = False
                    context["error"] = order_data


            except Exception as e:
                print(f"Error {e}")
                print(traceback.format_exc())
                context["payment_success"] = False
                context["error"] = str(e)

        return context


class CancelPaymentView(TemplateView):
    template_name = "patients/cancel.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["BASE_URL"] = settings.BASE_URL
        context["page_title"] = "Cancel Payment"

        appointment_id = self.request.GET.get("appointment_id")

        if appointment_id:
            try:
                appointment = Apointment.objects.get(id=appointment_id)
                PaymentHistory.objects.filter(
                    patient=appointment.patient,
                    appDate=appointment.appdate,
                    appTime=appointment.apptime
                ).update(status="3")  # Failed / Cancel
                appointment.status = "3"  # Cancel
                appointment.save()
            except:
                pass

        return context



#  show the appointment here 

class AllAppointmentView(TemplateView):

    def get_context_data(self , **kwargs):
        context = TemplateLayout.init(self , super().get_context_data(**kwargs))
        context["page_title"] = 'View Appointments'
        context["BASE_URL"] = settings.BASE_URL

        return context


class ViewAppointmentView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["BASE_URL"] = settings.BASE_URL
        context["page_title"] = "Cancel Payment"
        return context

class AppointmentDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["BASE_URL"] = settings.BASE_URL
        context["page_title"] = "Cancel Payment"

        pk =  self.kwargs.get('pk')

        appointment  = Apointment.objects.select_related(
                'doctor',
                'patient__patient',
            ).prefetch_related(
                "payment_appointment"
            ).get(id=pk)
        
        
        
        patient = appointment.patient
        user = appointment.patient.patient
        doctor = appointment.doctor

        payment_history = getattr(appointment, "payment_appointment", None)


        # print(f"Here {payment_history}")

        context["appointment"] = appointment
        context["patient"] = patient
        context["user"] = user
        context["doctor"] =  doctor
        context["paymenthistory"] =  payment_history

        return context
    

    def post(self, request, *args, **kwargs):
        try:
            appointment_id = request.POST.get("appointment_id")
            appointment_status = request.POST.get("appointment_status")

            appointment = get_object_or_404(Apointment, id=appointment_id)
            appointment.is_active = appointment_status
            appointment.save()

            return redirect("view_appointment_details", pk=appointment_id)

        except Exception:
            print(traceback.format_exc())
            return redirect("view_appointment_details", pk=self.kwargs.get("pk"))
