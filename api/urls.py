from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView 

router =  DefaultRouter()
router.register('clinics' , views.ClinicListSet , basename='clinics')

doctorouter =  DefaultRouter()
doctorouter.register('doctors' , views.DoctorView , basename='doctors')

urlpatterns =[
    path('' , include(router.urls) ) ,
    path("", include(doctorouter.urls)) ,
    path('get-clinic-users/' , views.ClinicAdminUsers.as_view() , name='get_clinic_users' ),

    path("patients/" , views.PatientListView.as_view() , name='patients_list') ,

    ## get available slot for the clinic
    path('get-available-clinic-slots/' , views.ClinicAvailableTimeSlots.as_view() , name="clinic_available_time_slots") ,
    path('get-appointment/' , views.GetAppointmentView.as_view() , name="get_appointment_status"),
    path('appointment/cancel/' , views.CancelAppointmentView.as_view() , name="appointment_cancel"),

    ## paypal
    path('paypal/create-order/' , views.CreatePaypalOrderView.as_view() , name="create_paypalorder"),


    ## get access token for the apis
    path("token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    ## dashboard data
    path('revenue-data/' , views.RevenueView.as_view() , name="revenue_data"),
]