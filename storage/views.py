from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings

from .models import UploadedFile
# Create your views here.
class UploadView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            uploaded_files = request.FILES.getlist('file')

            for file in uploaded_files:
                new_file = UploadedFile(file=file, user=request.user)
                new_file.save()

            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)