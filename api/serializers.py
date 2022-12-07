from .models import Item, SubItem, Pet, Reminder
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
#use password validation in next iteriation
#add here validation of pass with lenght, special char, etc
from django.contrib.auth.password_validation import validate_password

class ReminderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reminder
    fields = '__all__'
    read_only_fields = ("id",) 

  def validate(self, attrs):
    # wprowadzić walizację wszystkich parametrów (poza UUID)
    if len(attrs['name'])<3:
      raise ValidationError("Name too short.")
    return super().validate(attrs)

class PetSerializer(serializers.ModelSerializer):
  reminders = ReminderSerializer(many=True, required=False, )
  class Meta:
    model = Pet
    fields = ['id', 'name', 'type', 'desc', 'photo', 'birthdate', 'icon', 'color' ,'reminders']
    read_only_fields = ("id",)
    extra_kwargs = {
      'reminders': {'required': False}
    }

  #to chyba właściwie nie działa XD
  def validate(self, attrs):
    # wprowadzić walizację wszystkich parametrów (poza UUID)
    if len(attrs['name'])<3:
      raise ValidationError("Name too short.")
    pet_exists = User.objects.filter(username=attrs['name']).exists()
    if pet_exists:
      raise ValidationError("Username has already been used")
    return super().validate(attrs)

  def create(self, validated_data):
    pet = Pet.objects.create(**validated_data)
    if validated_data.get('reminders', None) is not None:
      subitems_data = validated_data.pop('reminders')
      for subitem_data in subitems_data:
        Reminder.objects.create(pet=pet, **subitem_data)
    return pet

  # def update(self, instance, validated_data):
  #   reminders = validated_data.pop('reminders')
  #   instance.save()
  #   return instance

  # def delete(self, instance, validated_data):
  #   pass


  """
  def update(self, instance, validated_data):
    subItems_data = validated_data.pop('items')
    instance.name = validated_data.get('name', instance.name)
    instance.save()
    # many contacts
    for contact_data in subItems_data:
      contact = SubItem.objects.get(pk=contact_data['id']) # this will crash if the id is invalid though
      contact.name = contact_data.get('name', contact.name)
      contact.save()
    return instance
  """
class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  class Meta:
    model = User
    fields = ('username', 'email', 'password')

  def validate(self, attrs):
    userpassword = attrs['password']
    #zdublownie z class User(models.Model)?
    if len(userpassword)<5:
      raise ValidationError("Pasword to short!")
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
    
class SubItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = SubItem
    fields = '__all__'
 
class ItemSerializer(serializers.ModelSerializer):
  subitems = SubItemSerializer(many=True, required=False, read_only=False)
  class Meta:
    model = Item
    fields = ['id', 'name', 'created', 'subitems']
    extra_kwargs = {
        'subitems': {'required': False}
    }
  def create(self, validated_data):
    item = Item.objects.create(**validated_data)
    if validated_data.get('subitems', None) is not None:
      subitems_data = validated_data.pop('subitems')
      for subitem_data in subitems_data:
        SubItem.objects.create(item=item, **subitem_data)
    return item