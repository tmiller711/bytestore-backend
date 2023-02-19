from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class UploadView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        print(request.user)
        print(request.data)

        return Response(status=status.HTTP_200_OK)