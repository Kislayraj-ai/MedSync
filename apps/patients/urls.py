from django.urls import path , reverse_lazy
from .views import PatientAdd  , PatientEdit , AddAppointmentView
from django.views.generic import RedirectView

urlpatterns = [
    path("" , RedirectView.as_view(url=reverse_lazy("add_appointment"))) ,
    path("view-patients/" , PatientAdd.as_view(template_name="patients/view_patients.html") , name='view_patients' ) ,
    # path("add-patient" , PatientAdd.as_view(template_name="patients/add_patient.html") , name='add_patient' ),

    # <int:pk>/
    path("edit-patient-appointment/" , PatientEdit.as_view(template_name="patients/edit_patient.html") , name='patient_edit' ),

    ## add appointment
    path("add-appointment" , AddAppointmentView.as_view(template_name="patients/add_appointment.html") , name='add_appointment' ),

]