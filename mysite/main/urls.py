from django.urls import path
from .views import *

app_name = "main"   


urlpatterns = [
    path("", homepage, name="homepage"),

    path("register", RegisterStudentView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", logout_request, name= "logout"),
    path("password_reset", password_reset_request, name="password_reset")
]