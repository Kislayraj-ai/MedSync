from django.urls import path
from .views import PatientAdd  , PatientEdit

urlpatterns = [
    path("" , PatientAdd.as_view(template_name="patients/view_patients.html") , name='view_patients' ) ,
    path("add-patients" , PatientAdd.as_view(template_name="patients/add_patient.html") , name='patient_add' ),

     path("edit-patient/<int:pk>/" , PatientEdit.as_view(template_name="patients/edit_patient.html") , name='patient_edit' )

]