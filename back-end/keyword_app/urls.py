from django.urls import path
from .views import CreateKeyword

urlpatterns = [
    path("create/", CreateKeyword.as_view(), name="create-keyword"),
]