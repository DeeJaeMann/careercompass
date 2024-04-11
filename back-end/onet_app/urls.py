from django.urls import path
from .views import DetailsInfo

urlpatterns = [
    path("<int:id>/", DetailsInfo.as_view(), name="occupation-details"),
]