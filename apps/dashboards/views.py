from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.conf import settings
from django.utils.timezone import now, timedelta
from apps.patients.models import PaymentHistory , Apointment
from django.db.models import Sum , Q
from api.utility import get_user_clinic_ids
from apps.clinics.models import AdminUserProfile , DoctorProfile


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class DashboardsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['BASE_URL'] =  settings.BASE_URL

        today = now().date()
        yesterday = today - timedelta(days=1)

        clinic_ids = []

        # total patients today
        appointment = Apointment.objects.filter(
            created_at__year=today.year,
            created_at__month=today.month
        )

        # Today’s revenue
        today_revenue = PaymentHistory.objects.filter(
            paid_on__date=today
        )

        # Yesterday’s revenue
        yesterday_revenue = PaymentHistory.objects.filter(
            paid_on__date=yesterday
        )

        if not self.request.user.is_superuser :
            clinic_ids = get_user_clinic_ids(self.request.user , AdminUserProfile , DoctorProfile)
            today_revenue = today_revenue.filter(appointment__doctor__doctor_profile__clinic_id__in=clinic_ids)
            yesterday_revenue = today_revenue.filter(appointment__doctor__doctor_profile__clinic_id__in=clinic_ids)

            appointment =  appointment.filter(doctor__doctor_profile__clinic_id__in=clinic_ids)

        today_revenue =  today_revenue.aggregate(total=Sum("amount"))["total"] or 0
        
        yesterday_revenue = yesterday_revenue.aggregate(total=Sum("amount"))["total"] or 0



        # Calculate percentage change
        if yesterday_revenue > 0:
            change_percent = ((today_revenue - yesterday_revenue) / yesterday_revenue) * 100
        else:
            change_percent = 100 if today_revenue > 0 else 0


        context['today_revenue'] = today_revenue
        context['change_percent'] =  round(change_percent, 2)
        context['is_positive'] = change_percent >= 0
        context['appointment'] = appointment.count()
        
        return context
