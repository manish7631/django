from django.urls import path
from . import views

urlpatterns = [    
    path('signary/', views.SignaryListAPIView.as_view(), name='signaryview'),  
    path('seq/', views.SequenceListAPIView.as_view(), name='sequenceview'),
]