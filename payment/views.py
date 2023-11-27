import requests
from django.http import HttpRequest, HttpResponse
from order.models import *
from account.models import *
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404, render
from .paystack import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


@api_view(['GET'])
def get_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    serializer = PaymentSerializer(payment, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buiness_payments(request):
    payments = Payment.objects.filter(user=request.user)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_client_payments(request, client_id):
    client = Client.objects.get(id=client_id)
    if client.user == request.user:
        payments = Payment.objects.filter(client=client)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    paystack = Paystack()
    status, result = paystack.verify_payment(payment.ref, payment.amount)
    if status:
        if result["amount"] / 100 == payment.amount:
            channel = result["channel"]
            payment.verified = True
            payment.payment_method = channel
            payment.save()
    if payment.verified:
        order = Order.objects.get(pk=payment.order.pk)
        order.billing_status = True
        order.save()
        payment.save()
        Notification.objects.create(
                level= 'success',
                recipient = payment.user,
                actor_content_type = ContentType.objects.get_for_model(order),
                verb= "An order invoice has been paid succesfully",
                actor_object_id = order.id,
            )
    else:
        Notification.objects.create(
                level= 'success',
                recipient = payment.user,
                actor_content_type = ContentType.objects.get_for_model(order),
                verb= "An order invoice is yet to be paid",
                actor_object_id = order.id,
            )
    serializer = PaymentSerializer(payment, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def initiate_payment(request: HttpRequest, pk) -> HttpResponse:
    order = Order.objects.get(pk=pk)
    business = User.objects.get(pk=order.user.id)
    if Payment.objects.filter(order=order).exists():
        payment = Payment.objects.get(order=order)
        # if payment.verified == True:
        #     serializer = PaymentSerializer(payment, many=False)
        #     return Response(serializer.data)
        # else:
        #     verify_payment(request, payment.ref)
        #     serializer = PaymentSerializer(payment, many=False)
        #     return Response(serializer.data)
        serializer = PaymentSerializer(payment, many=False)
        return Response(serializer.data)
    else:
        payment = Payment.objects.create(
            user = business, 
            client = order.client,
            amount = order.amount,
            email =  order.client.email,
            phone = order.client.contact,
            address = order.client.address,
            order = order,
        )
        # verify_payment(request, payment.ref)
        serializer = PaymentSerializer(payment, many=False)
        return Response(serializer.data)

    



      








        
      

