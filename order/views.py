from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.models import Notification
import datetime
from django.contrib.contenttypes.models import ContentType


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request, client_id):
    client = Client.objects.get(id =client_id)
    serializer = CreateOrderSerializer(data=request.data)
    if serializer.is_valid(): 
        if client.user == request.user:
            order = Order.objects.create(
                user = client.user,
                client=client,
                order_type= serializer.data['order_type'],
                description= serializer.data['description'],
                due_date= serializer.data['due_date'],
                amount= serializer.data['amount'],
                )
            Notification.objects.create(
                level= 'success',
                recipient = request.user,
                actor_content_type = ContentType.objects.get_for_model(order),
                verb= "An order invoice has been created",
                actor_object_id = order.id,
            )
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response("Unauthorized")
    return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.user == order.client or order.user:
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    else:
        return Response("Unauthorized")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buiness_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    
    for order in orders:
        if order.billing_status == False and datetime.datetime.now().date() > order.due_date:
            Notification.objects.create(
                level= 'success',
                recipient = request.user,
                actor_content_type = ContentType.objects.get_for_model(order),
                verb= "An order invoice has been paid",
                actor_object_id = order.id,
            )
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unpaid_buiness_orders(request):
    orders = Order.objects.filter(user=request.user, billing_status=False)
    serializer = OrderSerializer(orders, many=True)
    for order in orders:
        Notification.objects.create(
            level= 'success',
            recipient = request.user,
            actor_content_type = ContentType.objects.get_for_model(order),
            verb= "An order invoice has been paid",
            actor_object_id = order.id,
        )
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_paid_buiness_orders(request):
    orders = Order.objects.filter(user=request.user, billing_status=True)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_buiness_orders(request, client_id):#for all clients invoices
    client = Client.objects.get(id=client_id)
    if client.user == request.user:
        orders = Order.objects.filter(client=client)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    return Response('Unauthorized')

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.user == request.user:
        order.delete()
        return Response('Order deleted successfully')


