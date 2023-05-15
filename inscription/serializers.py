from rest_framework import serializers

from .models import Signary, Sequence



class SignarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Signary
        fields = '__all__'
        

class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        fields = '__all__'