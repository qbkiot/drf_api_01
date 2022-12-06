from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .models import Item, User, Pet, Reminder
from .serializers import ItemSerializer, UserSerializer, PetSerializer
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

#token b8fb864909b667a75d7410a9dd3ed202418e22a1

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@permission_classes((AllowAny,))
class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request: Request):
        data = request.data
        serializer=self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response={
                "message": "Created succesfully",
                "data" : serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):  
    return Response({'token': 'in database'},status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
def getPets(request):
    items = Pet.objects.all()
    serializer = PetSerializer(items, many = True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((AllowAny,))
def add_pet(request):
    serializer = PetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response('Succesfully aded pet')
    else:
        return Response('There was unexpected error.')

@api_view(['GET'])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
def getData(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def addItem(request):
    serializer = ItemSerializer(data=request.data)
    name_to_create = request.data.get("name")
    if Item.objects.filter(name = name_to_create).exists():
        return Response({"error":"user already exist"})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response('There was unexpected error.')


@api_view(['PUT'])
def editItem(request, name):
    if Item.objects.filter(name = name).exists():
        item = Item.objects.get(name=name)
        serializer = ItemSerializer(instance=item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('succesful')
        else:
            return Response({"error":"validation error"})
    else:
        return Response({"error":"can't find that name ;("})

@api_view(['DELETE'])
def deleteItem(request, name):
    item = Item.objects.filter(name = name)
    if item.exists():
        item.delete()
        return Response('success')
    else:
        return Response({"error":"can't find that name ;("})

@api_view(['DELETE'])
def deleteAll(request):
    Item.objects.all().delete()
    return Response({"error":"succesfully deleted all"})    

