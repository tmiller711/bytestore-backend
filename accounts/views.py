from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login

from .serializers import LoginSerializer, RegisterAccountSerializer
# Create your views here.
class Register(APIView):
    def post(self, request):
        print('test')

        return Response(status=status.HTTP_200_OK)

class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            account = authenticate(request, email=email, password=password)
            if account == None:
                return Response({"Invalid Credentials": "Could not authenticate user"}, status=status.HTTP_404_NOT_FOUND)
            
            login(request, account)

            return Response(status=status.HTTP_200_OK)