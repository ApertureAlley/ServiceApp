from rest_framework import serializers
from .models.custom_user import CustomUser
from .models.custom_user import Location
from .models.otp import Otp
from .models.service_provider_profile import ServiceProviderProfile
from .models.business_owner_profile import BusinessOwnerProfile
from django.contrib.auth.hashers import make_password

class LocationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Location
    fields = ['state', 'city']


class CustomUserSerializer(serializers.ModelSerializer):
  location = LocationSerializer(required=False)

  class Meta:
    model = CustomUser
    fields = ['id','email', 'password', 'first_name', 'last_name', 'contact_no', 'address', 'role', 'location']

  def create(self, validated_data):
    validated_data['password'] = make_password(validated_data['password'])
    location_data = validated_data.pop('location', None)
    if location_data != None:
      location, created = Location.objects.get_or_create(**location_data)
      user = CustomUser.objects.create(location=location, **validated_data)
    else:
      user = CustomUser.objects.create(**validated_data)      
    return user

  def update(self, instance, validated_data):
    location_data = validated_data.pop('location', None)
    if location_data != None:
      location, created = Location.objects.get_or_create(**location_data)
      instance.location = location
    password =  validated_data.pop('password', None)
    if password != None:
      instance.password = make_password(password)
    for attr, value in validated_data.items():
      setattr(instance, attr, value)
    instance.save()
    return instance

class OtpSerializer(serializers.ModelSerializer):
  class Meta:
    model = Otp
    fields = '__all__'


class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField()
  class Meta:
    model = CustomUser
    fields = ["email", "password"]

class ServiceProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderProfile
        exclude = ['user']  # Exclude 'user' from the fields since it's set internally

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.custom_user

        if not user:
            raise serializers.ValidationError("User not authenticated.")
        
        return ServiceProviderProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class BusinessOwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessOwnerProfile
        exclude = ['user']  # Exclude 'user' from the fields since it's set with current user

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.custom_user
        if not user:
            raise serializers.ValidationError("User not authenticated.")
        
        return BusinessOwnerProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
