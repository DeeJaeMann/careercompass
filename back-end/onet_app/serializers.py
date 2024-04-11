from rest_framework.serializers import ModelSerializer
from .models import Details, Knowledge, Education

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