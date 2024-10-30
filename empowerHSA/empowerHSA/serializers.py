from rest_framework import serializers
from empowerHSA.models import Lesson
from bson import ObjectId

class LessonSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
