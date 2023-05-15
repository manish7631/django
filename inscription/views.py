from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework import permissions
# from django.contrib.auth import get_user_model
from .models import Signary, Sequence
from .serializers import SignarySerializer, SequenceSerializer


# CustomUser = get_user_model()
class SignaryListAPIView(ListAPIView):
    # permission_classes=[permissions.IsAuthenticated]
    serializer_class = SignarySerializer

    def get_queryset(self):
        queryset = Signary.objects.all()        
        return queryset



class SequenceListAPIView(ListAPIView):
    # permission_classes=[permissions.IsAuthenticated]
    serializer_class = SequenceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['seq_in_num','site','artefact_type','material_type','field_symbol']
    filterset_fields = ['seq_in_num','site','field_symbol']
    search_fields = ['seq_in_num', 'site']
    ordering_fields = ['seqid', 'site']
    # ordering = ['seqid']

    def get_queryset(self):
        queryset = Sequence.objects.all()
        return queryset
