from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item
from .serializers import ItemSerializer
from django.http import HttpResponse
import json

@api_view(['GET'])
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