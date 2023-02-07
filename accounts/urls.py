from django.urls import path
import uuid

from .views import Login, Register, Activate

urlpatterns = [
    path('login/', Login.as_view()),
    path('register/', Register.as_view()),
    path('activate/<uidb64>/<token>/', Activate.as_view(), name='activate'),
]