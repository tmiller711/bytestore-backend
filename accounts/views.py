from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import IntegrityError

from .serializers import LoginSerializer, RegisterAccountSerializer, UserSerializer
from .models import Account
from .tokens import accounts_activation_token

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

            url = Account.get_activate_url(request, account)
            message = render_to_string("template_activate_account.html", {
                "url": url
            })
            mail_subject = "Activate Your Account"
            email_message = EmailMessage(mail_subject, message, to=[email])

            try:
                email_message.send()
            except:
                account.delete()
                return Response({"error": f"failed to send email to '{email}'"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # send_email_task.delay(mail_subject, message, email)

            return Response({"success": "Please confirm your email address"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Activate(APIView):

    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except:
            user = None

        if user is not None and accounts_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return Response(status=status.HTTP_200_OK)
            
        else:
            # alert the user of bad activation link
            return Response(status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # logout(request)
            authorization_header = request.headers.get("Authorization")
            bearer, token = authorization_header.split(" ")
            token = AccessToken(token)
            token.blacklist()
            print("test")
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer