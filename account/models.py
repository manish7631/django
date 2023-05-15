from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
import secrets
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from django.utils.encoding import force_str, force_bytes


# from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)    
    affiliation = models.CharField(max_length=200)    
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_email_verified = models.BooleanField(default=False)
    tc = models.BooleanField(default=False)
    reset_password_token = models.CharField(max_length=100, null=True, blank=True)
    reset_password_token_created_at = models.DateTimeField(null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'affiliation']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def is_active(self):
        return self.is_email_verified
    
    # def send_verification_email(self):
    #     subject = 'Verify your email'
    #     message = 'Please click the link below to verify your email.\n\n'
    #     message += f'http://localhost:8000/auth/verifyemail/{self.id}/'
    #     from_email = 'ashraf.epigraphy@gmail.com'
    #     # recipient_list = [self.email]
    #     recipient_list = ['nextgendoctors@gmail.com']
    #     send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    def send_verification_email(self):
        subject = 'Verify your email'
        message = 'Please click the link below to verify your email.\n\n'
        token = default_token_generator.make_token(self)
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        verify_url = reverse('verify_email_function_view', kwargs={'uidb64': uid, 'token': token})
        verify_url = f'{settings.BASE_URL}{verify_url}'
        message += verify_url
        from_email = 'ashraf.epigraphy@gmail.com'
        # recipient_list = [self.email]
        recipient_list = ['nextgendoctors@gmail.com']
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)



    def verify_email(self):
        self.is_email_verified = True
        self.save()

    def generate_password_reset_token(self):
        token = secrets.token_hex(32)
        self.reset_password_token = token
        self.reset_password_token_created_at = timezone.now()
        self.save(update_fields=['reset_password_token', 'reset_password_token_created_at'])
        return token


