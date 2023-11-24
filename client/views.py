from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid(): 
        serializer.save()
        client = Client.objects.get(id=serializer.data['id'])
        client.user = request.user
        client.save()
        serializer = ClientSerializer(client, many=False)
        return Response(serializer.data)
    return Response(serializer.errors)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_client(request, client_id):
    client = Client.objects.get(id=client_id)
    if client.user == request.user:
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            client = Client.objects.get(id=serializer.data['id'])
            client.user = request.user
            client.save()
            serializer = ClientSerializer(client, many=False)
            return Response(serializer.data)
        return Response(serializer.errors)
    return Response('Unauthorized')




@api_view(['GET'])
def get_client(request, client_id):
    client = Client.objects.get(id=client_id)
    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_business_clients(request):
    clients = Client.objects.filter(user=request.user)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_client(request, client_id):
    client = Client.objects.get(id=client_id)
    if client.user == request.user:
        client.delete()
        return Response('Order deleted successfully')
    return Response('Unauthorized')

