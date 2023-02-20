from django.db import models
from django.contrib.auth import get_user_model

def file_path(instance, filename):
    return f"{instance.user.id}/{filename}"

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to=file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    # add a class method for getting the file download link