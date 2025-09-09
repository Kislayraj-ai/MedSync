

def get_user_clinic_ids(authuser , AdminUserProfile , DoctorProfile):
        """
            Return list of clinic_ids for a given authenticated user.
            - Admin → clinics from AdminUserProfile
            - Doctor → clinics from DoctorProfile
        """
        user_role = authuser.roles.first()
        clinic_ids = []

        if user_role and user_role.role.id == 1:
            clinic_ids = AdminUserProfile.objects.filter(user=authuser).values_list("clinic_id", flat=True)
        else:
            clinic_ids = DoctorProfile.objects.filter(user=authuser).values_list("clinic_id", flat=True)

        return clinic_ids
