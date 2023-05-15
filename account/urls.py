from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from account.views import(
    RegisterApiView, LogoutApiView,
    ForgotPasswordAPIView, PasswordResetAPIView, verify_email_function_view,
)



urlpatterns = [    
    path('login/', TokenObtainPairView.as_view(), name='login_view'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('register/', RegisterApiView.as_view(), name='registerapiview'),
    path('register/', RegisterApiView.as_view(), name='registerapiview'),
    path('verifyemail/<str:uidb64>/<str:token>/', verify_email_function_view, name='verify_email_function_view'),
    path('logout/', LogoutApiView.as_view(), name='rest_logout'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', PasswordResetAPIView.as_view(), name='reset-password'),

]

