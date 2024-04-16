from django.urls import path
from .views import CreateKeyword, KeywordInfo, KeywordAllInfo

urlpatterns = [
    path("", KeywordAllInfo.as_view(), name="user-keywords"),
    path("<int:id>/", KeywordInfo.as_view(), name="keyword"),
    path("create/", CreateKeyword.as_view(), name="create-keyword"),
]
