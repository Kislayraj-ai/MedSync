from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import include

router =  DefaultRouter()
router.register('clinics' , views.ClinicListSet , basename='clinics')

doctorouter =  DefaultRouter()
doctorouter.register('doctors' , views.DoctorView , basename='doctors')

urlpatterns =[
    path('' , include(router.urls) ) ,
    path("", include(doctorouter.urls)) ,
    path("patients/" , views.PatientListView.as_view() , name='patients_list') ,

    ## get available slot for the clinic
    path('get-available-clinic-slots' , views.ClinicAvailableTimeSlots.as_view() , name="clinic_available_time_slots")
]