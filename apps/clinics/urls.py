from django.urls import path
from . import views

urlpatterns =[
    path("add-clinic/" , views.ClinicAdd.as_view(template_name="clinic/add_clinic.html") , name="add_clinic" ),
    path('view-clinic/' , views.ClinicView.as_view(template_name="clinic/view_clinics.html") , name="view_clinic"),
    path('edit-clinic/<int:pk>/', views.ClinicEdit.as_view(template_name="clinic/edit_clinic.html"), name="edit_clinic"),

    # doctors
    path("add-clinic-user/" , views.DoctorAdd.as_view(template_name="clinic/add_doctors.html") , name="add_clinic_user" ),
    path('view-clinic-user/' , views.DoctorViewList.as_view(template_name="clinic/view_doctors.html") , name="view_clinic_user"),
    path('edit-doctor/<int:pk>/', views.DoctorViewEdit.as_view(template_name="clinic/edit_doctor.html"), name="edit_doctor"),

    # clinic admin user
    # path("add-admin-user/" , views.AdminUser.as_view(template_name="clinic/add_admin_user.html") , name="add_admin_user" ),

]
