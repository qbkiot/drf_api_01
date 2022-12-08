from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from .models import Item, SubItem, Pet, Reminder


# Need this while using custom user model
from django.contrib.auth import get_user_model
User = get_user_model()


"""

--- REMINDER  SERIALIZER---

"""

class ReminderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reminder
    fields = '__all__'
    read_only_fields = ('id',) 

  def validate(self, attrs):
    # wprowadzić walizację wszystkich parametrów (poza UUID)
    if len(attrs['name'])<3:
      raise ValidationError("Name too short.")
    return super().validate(attrs)

"""

--- PET  SERIALIZER---

"""
class PetSerializer(serializers.ModelSerializer):
  reminders = ReminderSerializer(many=True, required=False, )
  class Meta:
    model = Pet
    #fields = ['id', 'owner', 'name', 'type', 'desc', 'photo', 'birthdate', 'icon', 'color' ,'reminders']
    fields = '__all__'
    read_only_fields = ('id',)
    extra_kwargs = {
      'reminders': {'required': False}
    }

  def validate(self, attrs):
    # wprowadzić walizację wszystkich parametrów (poza UUID)
    if len(attrs['name'])<3:
      raise ValidationError("Name too short.")
    user_exists = User.objects.filter(id=attrs['owner']).exists()
    print(User.objects.filter(id=attrs['owner']))
    print(f"user_exists")
    if not user_exists:
      raise ValidationError("Owner do not exist")
    return super().validate(attrs)

  def create(self, validated_data):
    pet = Pet.objects.create(**validated_data)
    if validated_data.get('reminders', None) is not None:
      subitems_data = validated_data.pop('reminders')
      for subitem_data in subitems_data:
        Reminder.objects.create(pet=pet, **subitem_data)
    return pet

"""

--- USER  SERIALIZER---

"""

class UserSerializer(serializers.ModelSerializer):
  
  #validate if username is alphanumeric
  alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
  username = serializers.CharField(max_length=20, validators=[alphanumeric])

  #validate password in not longer than 20 signs
  password = serializers.CharField(max_length=20, write_only=True)
  class Meta:
    model = User
    fields = ('username', 'email', 'password')

  def validate(self, attrs):
    # client side validation if password == re_password
    password = attrs['password']

    if len(password) < 6:
      raise ValidationError("Password is too short! Use min. 6 characters!")
    
    # check if user with this name exists in database
    user_exists = User.objects.filter(username=attrs['username']).exists()
    if user_exists:
      raise ValidationError("Username has already been used")

    # check if user with this e-mail exists in database
    email_exists = User.objects.filter(email=attrs['email']).exists()
    if email_exists:
      raise ValidationError("This e-mail is in use. If you got account - remind password.")

    # if validation is succeed -> go to user creation
    return super().validate(attrs)



  def create(self, validated_data):

    # Use pop() when you need one time validation check & will not use the data further.
    password = validated_data.pop("password")

    # create user instance ??
    user = super(UserSerializer, self).create(validated_data)
    
    # set user password
    user.set_password(password)

    # save user
    user.save()

    #generate token for user to perform requests
    Token.objects.create(user=user)

    return user


"""

--- OLD TEST ITEMS ---

"""
    
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