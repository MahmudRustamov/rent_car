from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.accounts.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email',"username",'phone_number','bio','profile_image']
        extra_kwargs = ['is_active']

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match!'})
        return attrs

    @staticmethod
    def validate_phone_number(value):
        if not value.startswith('+998'):
            raise serializers.ValidationError("Phone number must start with +998")
        elif len(value) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        return value

    @staticmethod
    def validate_username(value):
        for sign in value:
            if not (sign.isalnum() or sign == '_'):
                raise serializers.ValidationError("Username must contain only letters numbers and '_'")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,attrs):
        credentials = {
            "username":attrs.get('username'),
            "password":attrs.get('password')
        }

        user = authenticate(request=self.context['request'], **credentials)
        if user is None:
            raise serializers.ValidationError("Username or password is incorrect")
        else:
            attrs['user'] = user
            return attrs