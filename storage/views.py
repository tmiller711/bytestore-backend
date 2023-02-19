from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings

# Create your views here.
class UploadView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        uploaded_files = request.FILES.getlist('file')

        # Get the user's media folder
        user_folder = os.path.join(settings.MEDIA_ROOT, str(request.user.id))

        # Create the user's media folder if it doesn't exist
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Save the uploaded file to the user's media folder
        for file in uploaded_files:
            file_path = os.path.join(user_folder, file.name)
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

        return Response(status=status.HTTP_200_OK)