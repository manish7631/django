from rest_framework import serializers
from django.contrib.auth import get_user_model


CustomUser = get_user_model()

class CustomUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'affiliation', 'password', 'password2']
        # field = '__all__'
        extra_kwargs={
            'password':{'write_only':True},
            'password2':{'write_only':True}
        }
    
    def create(self, validated_data):
        email = validated_data.get('email')        
        name = validated_data.get('name')
        affiliation = validated_data.get('affiliation')
        password = validated_data.get('password')
        password2 = validated_data.get('password2')
        
        if password==password2:
            user = CustomUser(email=email, name=name, affiliation=affiliation)
            user.set_password(password)
            user.save()
            user.send_verification_email()
            return user
        else:
            raise serializers.ValidationError({'Error':'Passwords do not match!'})
        


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)