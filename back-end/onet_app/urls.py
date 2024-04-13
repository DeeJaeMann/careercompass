from django.urls import path
from .views import (
    DetailsInfo,
    KnowledgeInfo,
    EducationInfo,
    SkillsInfo
)

urlpatterns = [
    # NOTE This ID is the Occupation ID, not the Details ID
    path("<int:id>/", DetailsInfo.as_view(), name="occupation-details"),
    path("knowledge/<int:id>/", KnowledgeInfo.as_view(), name="get-knowledge"),
    path("education/<int:id>/", EducationInfo.as_view(), name="get-education"),
    path("skills/<int:id>/", SkillsInfo.as_view(), name="get-skills"),
]
