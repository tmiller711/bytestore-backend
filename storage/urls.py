from django.urls import path

from .views import UploadView, GetUploadedFiles

urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),
    path('getfiles/', GetUploadedFiles.as_view(), name='getfiles')
]