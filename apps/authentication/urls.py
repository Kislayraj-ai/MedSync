from django.urls import path
from .views import AuthView , logoutView


urlpatterns = [
    path(
        "login/",
        AuthView.as_view(template_name="auth_login_basic.html"),
        name="auth_login_basic",
    ),

    path(
        "logout/",logoutView,
        name="auth_logout_basic",
    ),

    path(
        "register/",
        AuthView.as_view(template_name="auth_register_basic.html"),
        name="auth-register-basic",
    ),
    path(
        "forgot_password/",
        AuthView.as_view(template_name="auth_forgot_password_basic.html"),
        name="auth-forgot-password-basic",
    ),
]
