from django.urls import path , reverse_lazy
from .views import PatientAdd  , PatientEdit , AddAppointmentView , CompletePaymentView , SuccessPaymentView , CancelPaymentView , AppointmentDetailView , AllAppointmentView , PatientDetailView
from django.views.generic import RedirectView

urlpatterns = [
    path("" , RedirectView.as_view(url=reverse_lazy("add_appointment"))) ,

    # appointment view all
    path("view-patients/" , PatientAdd.as_view(template_name="patients/view_patients.html") , name='view_patients' ) ,
    path("add-patient-appointment/" , PatientAdd.as_view(template_name="patients/add_patient.html") , name='add_patient' ),
    path("view-appointment/" , AllAppointmentView.as_view(template_name="patients/view_appointment.html") , name='view_appointment' ),
    path("appointment-details/<int:pk>/" , AppointmentDetailView.as_view(template_name="patients/view_appointment_details.html") , name='view_appointment_details' ),
    path("patient-detail/<int:pk>/" , PatientDetailView.as_view(template_name="patients/patient_detail.html") , name='patient_detail' ) ,

    # <int:pk>/
    path("edit-patient-appointment/" , PatientEdit.as_view(template_name="patients/edit_patient.html") , name='patient_edit' ),

    ## add appointmentadd-patient-appointment
    path("add-appointment/" , AddAppointmentView.as_view(template_name="patients/add_appointment.html") , name='add_appointment' ),
    path("complete-payment/" , CompletePaymentView.as_view(template_name="patients/complete_payment.html") , name='complete_payment' ),

    # payment action
    path("paypal/success-payment/" , SuccessPaymentView.as_view(template_name="patients/success.html") , name='success_payment' ),
    path("paypal/cancel-payment/" , CancelPaymentView.as_view(template_name="patients/cancel.html") , name='cancel_payment' ),


]
