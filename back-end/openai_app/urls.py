from django.urls import path
from .views import OpenAIOccupation

urlpatterns = [
    path("", OpenAIOccupation.as_view(), name="get-occupations"),
]
