from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
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


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    rentals_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','email','username','full_name','rentals_count']

    @staticmethod
    def get_full_name(obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    @staticmethod
    def get_rentals_count(obj):
        return obj.rentals.count()
