from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login

from .serializers import LoginSerializer, RegisterAccountSerializer
from .models import Account

# Create your views here.
class Register(APIView):
    serializer_class = RegisterAccountSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            username = serializer.data.get('username')
            password = serializer.data.get('password')

            account = Account(email=email, username=username)
            account.set_password(password)
            account.save()

            # url = Account.get_activate_url(request, account)
            # message = render_to_string("template_activate_account.html", {
            #     "url": url
            # })
            # mail_subject = "Activate Your Account"
            # send_email_task.delay(mail_subject, message, email)

            return Response({"success": "Please confirm your email address"}, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)

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