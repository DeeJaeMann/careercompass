from django.urls import path
from .views import SignUp, LogIn, LogOut

urlpatterns = [
    path("signup/", SignUp.as_view(), name="sign-up"),
    path("login/", LogIn.as_view(), name="login"),
    path("logout/", LogOut.as_view(), name="logout"),
]