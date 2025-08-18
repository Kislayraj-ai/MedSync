from django.urls import path
from . import views

urlpatterns =[
    path("add-clinic" , views.ClinicAdd.as_view(template_name="clinic/add_clinic.html") , name="add_clinic" ),
    path('view-clinic' , views.ClinicView.as_view(template_name="clinic/view_clinics.html") , name="view_clinic"),
    path('edit-clinic/<int:pk>/', views.ClinicEdit.as_view(template_name="clinic/edit_clinic.html"), name="edit_clinic"),

    # doctors
    path("add-doctors" , views.DoctorAdd.as_view(template_name="clinic/add_doctors.html") , name="add_doctors" ),
    path('view-doctors' , views.DoctorViewList.as_view(template_name="clinic/view_doctors.html") , name="view_doctors"),
    path('edit-doctor/<int:pk>/', views.DoctorViewEdit.as_view(template_name="clinic/edit_doctor.html"), name="edit_doctor"),
]
