from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "New passwords do not match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'profile_pic', 'address','city', 'state', 'Country']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()  # Nesting the profile serializer

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')

        # Create the User object
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()

        # Create the Profile object
        Profile.objects.create(user_id=user, **profile_data)

        return user
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)

        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        # Update Profile fields
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        return instance

