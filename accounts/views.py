from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class Register(APIView):
    def post(self, request):
        print('test')

        return Response(status=status.HTTP_200_OK)

class Login(APIView):
    def post(self, request):
        print('test')

        return Response(status=status.HTTP_200_OK)