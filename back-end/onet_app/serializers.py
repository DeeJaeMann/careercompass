from rest_framework.serializers import ModelSerializer
from .models import Details, Knowledge, Education, Skills


class DetailsSerializer(ModelSerializer):

    class Meta:
        model = Details
        fields = "__all__"


class KnowledgeSerializer(ModelSerializer):

    class Meta:
        model = Knowledge
        fields = "__all__"


class EducationSerializer(ModelSerializer):

    class Meta:
        model = Education
        fields = "__all__"


class SkillsSerializer(ModelSerializer):

    class Meta:
        model = Skills
        fields = "__all__"
