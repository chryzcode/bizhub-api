from django.shortcuts import render
from notifications.models import Notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notification_details(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if notification.recipient == request.user:
        serializer = NotificationSerializer(notification, many=False)
        return Response(serializer.data)
    return Response('Unauthorized')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_notifications(request):
    notification = Notification.objects.filter(recipient=request.user)
    serializer = NotificationSerializer(notification, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_notifications(request):
    notification = Notification.objects.filter(recipient=request.user, unread=True)
    serializer = NotificationSerializer(notification, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_read_notifications(request):
    notification = Notification.objects.filter(recipient=request.user, unread=False)
    serializer = NotificationSerializer(notification, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if notification.recipient == request.user:
        notification.unread = False
        notification.save()
        serializer = NotificationSerializer(notification, many=False)
        return Response(serializer.data)
    return Response('Unauthorized')



