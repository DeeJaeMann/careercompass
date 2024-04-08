from django.urls import path
from .views import CreateKeyword, KeywordInfo

urlpatterns = [
    path("create/", CreateKeyword.as_view(), name="create-keyword"),
    path("<int:id>/", KeywordInfo.as_view(), name="get-keyword"),
]