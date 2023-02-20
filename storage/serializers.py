from rest_framework import serializers
from .models import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        return obj.file.name.split('/')[-1]

    class Meta:
        model = UploadedFile
        fields = '__all__'
