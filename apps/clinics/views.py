from django.shortcuts import render , redirect
from django.views.generic import TemplateView
from web_project import TemplateLayout
from .models import Clinic , ClinicTime , DoctorProfile , UserRole , Roles , AdminUserProfile
from django.contrib import messages
from django.conf import settings
from datetime import date
# Create your views here.
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .forms import AdminUserForm


# def addClinic(request):
#     context = {}
#     context = TemplateLayout.init(request, context)
#     return render(request, "clinic/add_clinic.html", context)

def uniqueClinicId(name=''):
    prefix = "CLI"
    # clinicprefix = name[:3]

    ## get last clnic key
    lastclinic =  Clinic.objects.order_by('-id').first()
    today =  date.today()
    year = today.year 
    month = today.month
    cinicid =  f"{prefix}{year}{month}{lastclinic.id if lastclinic else 1 }"
    return cinicid

class ClinicAdd(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        clinicid = uniqueClinicId()
        # Apna custom data bhejna
        context["page_title"] = "Add New Clinic"
        context['clinic_id'] = clinicid
        return context


    def post(self,request , *args, **kwargs):
        try:
            name = request.POST.get("name")
            clinicid = request.POST.get("clinicid")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            logo = request.FILES.get("logo")
            is_active = request.POST.get("is_active") == "on"

            ## get the timing of the days

            if not name.strip() or not clinicid.strip() or not email.strip():
                    messages.warning(request , "Some Fileds are missing or empty !!")
                    return redirect('add_clinic')
            
            # print("Active " , is_active)
            clinic =  Clinic()
            clinic.name = name
            clinic.clinicid =  clinicid
            clinic.phone=phone
            clinic.email=email
            clinic.logo=logo
            clinic.is_active=is_active
            clinic.save()


            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_name_to_int = {
                    "Monday": 0,
                    "Tuesday": 1,
                    "Wednesday": 2,
                    "Thursday": 3,
                    "Friday": 4,
                    "Saturday": 5,
                    "Sunday": 6,
                }
            weekly_schedule = {}

            for day in days :
                day_lower =  day.lower()
                start_time =  request.POST.get(F"{day_lower}_start") or "00:00"
                end_time = request.POST.get(f"{day_lower}_end") or "00:00"
                weekly_schedule[day] =  {"start" : start_time , "end" : end_time}


            for day in days :
                times =  weekly_schedule[day]
                timing =  ClinicTime()

                try:
                    start_time = datetime.strptime(times['start'], "%H:%M").time()
                    end_time = datetime.strptime(times['end'], "%H:%M").time()
                except Exception as e:
                    print(f"Error on day {day}: times={times}, error={e}")
                    continue


                timing.clinic =  clinic
                timing.day = day_name_to_int[day] 
                timing.open_time =  start_time
                timing.end_time =  end_time

                
                timing.is_closed = 1 if (times['start'] == "00:00" and times['end'] == "00:00") else 0


                timing.save()


            messages.success(request ,  'Clinic has been added successfully !!')
            return redirect('add_clinic')

        except Exception as e :

            messages.error(request , f"Error :- {e}")
            return redirect('add_clinic')


class ClinicView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self , super().get_context_data(**kwargs))
        context["BASE_URL"] =  settings.BASE_URL
        return context

class ClinicEdit(TemplateView):

    def get_context_data(self,*args , **kwargs):
        context = TemplateLayout.init(self , super().get_context_data(**kwargs))

        pk =  self.kwargs.get('pk')

        try:
            clinic = Clinic.objects.prefetch_related('clinic_times').get(id=pk)
            clinic_info = {}


            clinic_info = {
                        "id": clinic.id,
                        "name": clinic.name,
                        "clinicid": clinic.clinicid,
                        "email" : clinic.email ,
                        "logo" : clinic.logo ,
                        "phone": clinic.phone,
                        "is_active" : clinic.is_active ,
                        "timings": {} 
                    }
            
            int_to_day_name = {
                   0 : "Monday" ,
                   1 :"Tuesday",
                   2 :"Wednesday",
                   3 :"Thursday",
                   4 :"Friday",
                   5 :"Saturday",
                   6 :"Sunday",
                }

            for time in clinic.clinic_times.all().order_by('day'):
                    clinic_info['timings'][int_to_day_name[time.day]] = {"start" : time.open_time , "end" : time.end_time}
            
            context["clinic"] = clinic_info


        except Exception as e:
            print(e)
        return context
    

    def post(self,request , *args, **kwargs):

        pkid =  request.POST.get('pkid')
        name = request.POST.get("name")
        clinicid = request.POST.get("clinicid")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        logo = request.FILES.get("logo")
        is_active = request.POST.get("is_active") == "on"
        

        if not name.strip() or not clinicid.strip() or not email.strip() or not pkid:
            messages.warning(request , "Some Fileds are missing or empty !!")
            return redirect('edit_clinic' , pkid)

        clinic =  Clinic.objects.get(id=pkid)
        clinic.name = name
        clinic.clinicid =  clinicid
        clinic.phone=phone
        clinic.email=email

        if logo :
            clinic.logo=logo
        
        clinic.is_active=is_active
        clinic.save()


        
        ClinicTime.objects.filter(clinic=clinic).delete()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_name_to_int = {
                    "Monday": 0,
                    "Tuesday": 1,
                    "Wednesday": 2,
                    "Thursday": 3,
                    "Friday": 4,
                    "Saturday": 5,
                    "Sunday": 6,
                }
        weekly_schedule = {}

        for day in days :
                day_lower =  day.lower()
                start_time =  request.POST.get(F"{day_lower}_start") or "00:00"
                end_time = request.POST.get(f"{day_lower}_end") or "00:00"
                weekly_schedule[day] =  {"start" : start_time , "end" : end_time}


        for day in days :
                times =  weekly_schedule[day]
                timing =  ClinicTime()

                try:
                    start_time = datetime.strptime(times['start'], "%H:%M").time()
                    end_time = datetime.strptime(times['end'], "%H:%M").time()
                except Exception as e:
                    print(f"Error on day {day}: times={times}, error={e}")
                    continue


                timing.clinic =  clinic
                timing.day = day_name_to_int[day] 
                timing.open_time =  start_time
                timing.end_time =  end_time

                
                timing.is_closed = 1 if (times['start'] == "00:00" and times['end'] == "00:00") else 0


                timing.save()



        messages.success(request ,  'Clinic has been updated successfully !!')
        return redirect('edit_clinic' , pkid)
    


## add the doctors
class DoctorAdd(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self , super().get_context_data(**kwargs))
        context["BASE_URL"] =  settings.BASE_URL
        context['page_title'] = 'Add Admin User'
        return context

    def post(self, request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            firstname = request.POST.get('first_name')
            lastname = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role_id = request.POST.get('role')

            specialization = request.POST.get('specialization')
            experience = request.POST.get('experience')
            fees = request.POST.get('fees')
            clinic_id = request.POST.get('clinic')

            ### creating user
            user = User.objects.create(
                username=username,
                first_name=firstname,
                last_name=lastname,
                email=email,
                password=make_password(password)
            )

            ### for roles here
            role = Roles.objects.get(id=role_id)
            UserRole.objects.create(user=user, role=role)

            
            ### roles based profiles here
            if role.name == Roles.RoleChoices.ADMIN:
                AdminUserProfile.objects.create(
                    user=user,
                    clinic_id=clinic_id,
                )
                messages.success(request, 'Admin has been added successfully !!')

            elif role.name == Roles.RoleChoices.DOCTOR:
                DoctorProfile.objects.create(
                    user=user,
                    specialization=specialization,
                    experience=experience,
                    fees=fees,
                    clinic_id=clinic_id
                )
                messages.success(request, 'Doctor has been added successfully !!')

            else:
                messages.warning(request, 'Only Admin and Doctor roles are supported here.')

            return redirect('view_clinic_user')

        except Exception as e:
            messages.error(request, f"Error :- {e}")
            return redirect('view_clinic_user')

class DoctorViewEdit(TemplateView):
    def get_context_data(self, **kwargs) :
        context = TemplateLayout.init(self , super().get_context_data(**kwargs))
        context["BASE_URL"] =  settings.BASE_URL
        context['page_title'] = 'Edit Admin User'

        pk = self.kwargs.get('pk')

        user_info = (
            User.objects
            .select_related("doctor_profile", "admin_profile")
            .prefetch_related("roles__role")
            .get(id=pk)
        )


        role = user_info.roles.first().role.name if user_info.roles.exists() else None
        # print("roles " , role)

        if role == Roles.RoleChoices.ADMIN:
            doctorprofile = user_info.admin_profile
        elif role == Roles.RoleChoices.DOCTOR:
            doctorprofile = user_info.doctor_profile

        # print()
        context['doctorinfo'] = user_info
        context['doctorprofile'] = doctorprofile
        context['role'] = role

        return context
    
    def post(self , request , *args, **kwargs):

        try:
            pkid =   request.POST.get('pkid')
            username =  request.POST.get('username')
            firstname = request.POST.get('first_name')
            lastname = request.POST.get('last_name')
            email = request.POST.get('email')
            role = request.POST.get('role')

            if not pkid:
                messages.error(request, "Doctor ID missing!")
                return redirect('edit_doctor' , pkid)

            specialization = request.POST.get('specialization')
            experience = request.POST.get('experience')
            fees = request.POST.get('fees')
            clinic = request.POST.get('clinic')

            # Create User
            user, created = User.objects.update_or_create(
                id=pkid,
                defaults={
                    'username': username,
                    'first_name': firstname,
                    'last_name': lastname,
                    'email': email
                }
            )

            ### for roles here
            role = Roles.objects.get(id=role)
            UserRole.objects.update_or_create(
                user=user,
                defaults={"role": role}
            )

            # Roles based profiles
            if role.id == Roles.RoleChoices.DOCTOR:   # Doctor role
                DoctorProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        "specialization": specialization,
                        "experience": experience,
                        "fees": fees,
                        "clinic_id": clinic,
                    },
                )
                messages.success(request ,  'Admin updated successfully !!')
            elif role.id == Roles.RoleChoices.ADMIN:
                AdminUserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        "clinic_id": clinic,
                    },
                )
                messages.success(request ,  'Admin updated successfully !!')

            
            return redirect('view_clinic_user')

        except Exception as e :
            messages.error(request , f"Error :- {e}")
            print(f"Error :- {e}")
            return redirect('view_clinic_user')


class DoctorViewList(TemplateView):
     
     def get_context_data(self, **kwargs):
         context = TemplateLayout.init(self , super().get_context_data(**kwargs))
         context["BASE_URL"] =  settings.BASE_URL
         context['page_title'] = 'View Admin User'
         return context


# class AdminUser(TemplateView):
#     def get_context_data(self, **kwargs):
#         context = TemplateLayout.init(self,super().get_context_data(**kwargs))
#         context["BASE_URL"] =  settings.BASE_URL
#         context['page_title'] = 'Add Admin User'
#         context['admin_form'] =  AdminUserForm()
#         return context

#     def post(self, request, *args, **kwargs):
#         try:
#             form = AdminUserForm(request.POST)
#             if form.is_valid():
#                 user = form.save(commit=False)
#                 user.set_password(form.cleaned_data['password'])
#                 user.save()

#                 # Assign ADMIN role
#                 admin_role = Roles.objects.get(name=Roles.ADMIN)
#                 UserRole.objects.create(user=user, role=admin_role)

#                 # Success message
#                 messages.success(request, f"Admin user '{user.username}' created successfully.")

#                 # Redirect back to the add admin page
#                 return redirect('add_admin_user')

#             else:
#                 # Form errors
#                 messages.error(request, "Please correct the errors below.")
#                 return render(request, 'your_template.html', {'form': form})

#         except Exception as e:
#             messages.error(request, f"An error occurred: {str(e)}")
#             return redirect('add_admin_user')
        


# class AdminUserList(TemplateView):
#     def get_context_data(self, **kwargs):
#         context = TemplateLayout.init(self,super().get_context_data(**kwargs))
#         context["BASE_URL"] =  settings.BASE_URL
#         context['page_title'] = 'View Admin User'

#         return context