from rest_framework.views import APIView
from rest_framework.response import Response
from account.serializers import (
    CustomUserRegisterSerializer,
    ForgotPasswordSerializer,
)
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
# from django.conf import settings
from django.urls import reverse

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse


class RegisterApiView(APIView):
    serializer_class = CustomUserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response_data = {
                'user': serializer.data,
            }

            # create an HTTP response
            response = Response(response_data, status=status.HTTP_201_CREATED)

            # set the access token in a cookie
            response.set_cookie('access_token', access_token, httponly=True)

            # return the HTTP response
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class RegisterApiView(APIView):
#     serializer_class = CustomUserRegisterSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data = request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)

#             response_data = {
#                 'refresh':str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': serializer.data,
#             }
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutApiView(APIView):
    """
    Logout user (add token to blacklist)
    """
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out.'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


CustomUser = get_user_model()

class ForgotPasswordAPIView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User with given email not found'}, status=status.HTTP_404_NOT_FOUND)
        
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        encoded_token = urlsafe_base64_encode(force_bytes(token))

        
        # Send an email with the new_password reset link
        reset_link = request.build_absolute_uri(reverse('reset-password')) + f'?email={email}&token={encoded_token}'
        send_mail(
            subject='Password Reset',
            message=f'Use the following link to reset your new_password: {reset_link}',
            #from_email=settings.DEFAULT_FROM_EMAIL,
            from_email = 'ashraf.epigraphy@gmail.com',
            #recipient_list=[email],            
            recipient_list = ['nextgendoctors@gmail.com'],
            fail_silently=False,
        )
        return Response({'detail': 'Password reset email sent'})
    



class PasswordResetAPIView(APIView):
    def post(self, request):
        
        email = request.data.get('email')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')

        if not all([email, token, new_password, new_password_confirm]):
            return Response({'detail': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User with given email not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verify the token
        token_generator = PasswordResetTokenGenerator()
        decoded_token = force_str(urlsafe_base64_decode(token))

        if not token_generator.check_token(user, decoded_token):
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != new_password_confirm:
            return Response({'detail': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password reset successful'})




def verify_email_function_view(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = get_object_or_404(CustomUser, pk=uid)

    if not default_token_generator.check_token(user, token):
        return HttpResponseBadRequest('Verification link is invalid!')

    user.is_email_verified = True
    user.save()
    return HttpResponse('Email verification successful!')