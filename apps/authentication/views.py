from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""


class AuthView(TemplateView):

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            }
        )

        return context
    
    def post(self , request):
        username_or_email = request.POST.get("email-username")
        password = request.POST.get("password")

        user = authenticate(request, username=username_or_email, password=password)


        if not user :
            try:
                u = User.objects.get(username=username_or_email)
                user = authenticate(request, username=u.username, password=password)

            except User.DoesNotExist:
                user = None

        if user is not None :
            login(request , user)
        else:
            messages.error(request, "Invalid username/email or password")

        return redirect("index")
    
def logoutView(request):
    logout(request)
    return redirect("auth_login_basic")
