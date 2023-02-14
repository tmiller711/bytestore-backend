from django.urls import path
import uuid
from rest_framework_simplejwt import views as jwt_views

from .views import Register, Activate, Logout
from .views import MyTokenObtainPairView

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('activate/<uidb64>/<token>/', Activate.as_view(), name='activate'),
]