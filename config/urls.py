from django.contrib import admin
from django.urls import include, path
from web_project.views import SystemView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),

    # Dashboard urls
    path("", include("apps.dashboards.urls")),

    # Clinic urls
    path('clinic/' , include("apps.clinics.urls") ) ,

    # apis endpoints
    path('api/v1/' , include('api.urls'))

] + static(settings.MEDIA_URL , document_root =  settings.MEDIA_ROOT)

handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
