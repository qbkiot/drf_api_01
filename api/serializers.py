from .models import Item
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
#use password validation in next iteriation
#add here validation of pass with lenght, special char, etc
from django.contrib.auth.password_validation import validate_password

class ItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = Item
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  class Meta:
    model = User
    fields = ('username', 'email', 'password')

  def validate(self, attrs):
    
    user_exists = User.objects.filter(username=attrs['username']).exists()
    email_exists = User.objects.filter(email=attrs['email']).exists()
    if user_exists:
      raise ValidationError("Username has already been used")
    if email_exists:
      raise ValidationError("Email has already been used XD")
    return super().validate(attrs)

  def create(self, validated_data):
    password = validated_data.pop("password")
    user = super(UserSerializer, self).create(validated_data)
    #user.set_password(validated_data['password'])
    user.set_password(password)
    user.save()
    Token.objects.create(user=user)
    return user
    
