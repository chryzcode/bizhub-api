import requests
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
# Create your views here.

@api_view(['GET'])
def all_users(request):
    if request.user.is_authenticated:
        all_users = User.objects.exclude(id=request.user.id)
    else:
        all_users = User.objects.all()
    serializer = UserSerializer(all_users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def a_user(request, slugified_business_name):
    user = User.objects.get(slugified_business_name=slugified_business_name)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def account_register(request):
    if request.user:
        request.user.auth_token.delete()
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(id=serializer.data['id'])
        user.set_password(user.password)
        user.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def account_update(request):
    user = request.user
    serializer = UpdateUserSerializer(user, data=request.data)
    if serializer.is_valid(): 
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def account_delete(request):
    user = request.user
    user.delete()
    return Response('User deleted successfully')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def account_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({'detail': 'Account succesfully logged out'}, status=status.HTTP_200_OK)




@api_view(['POST'])
def account_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = get_object_or_404(User, email=email)
            if user:
                user = authenticate(request, email=email, password=password)
                if user:
                    token, _ = Token.objects.get_or_create(user=user)
                    Notification.objects.create(
                        level= 'success',
                        recipient = request.user,
                        actor_content_type = ContentType.objects.get_for_model(user),
                        verb= "An order invoice has been created",
                        actor_object_id = user.id,
                    )
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                        return Response("User password is incorrect")
            else:
                return Response("User with email do not exist")
        except:
            return Response("User with email do not exist")




# def resolve_account_details(request, account_number, account_bank):
#     url = "https://api.flutterwave.com/v3/accounts/resolve"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": "Bearer " + settings.FLUTTERWAVE_SECRET_KEY,
#     }
#     data = {
#         "account_number": account_number,
#         "account_bank": account_bank,
#     }
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return False
    


# def get_all_banks(request):
#     flutterwave_currency_code = 'NG'
#     url = f"https://api.flutterwave.com/v3/banks/{flutterwave_currency_code}"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": "Bearer " + settings.FLUTTERWAVE_SECRET_KEY,
#     }
#     response = requests.get(url, headers=headers)
#     result = response.json().get("data")
#     return result


# class user_account_bank(APIView):
#     def post(self, request, account_number, bank_code):
#         banks = get_all_banks(request)
#         for bank in banks:
#             if bank_code == bank['code']:
#                 bank_name = bank['name']
#                 bank_code = bank['code']
#         response = resolve_account_details(request, account_number, bank_code)
#         account_name = response.get("data").get("account_name")
#         if not Bank_Info.objects.filter(user=request.user).exists():
#             bank_info = Bank_Info.objects.create(
#                 account_number = account_number,
#                 account_name = account_name,
#                 bank_name = bank_name,
#                 bank_code = bank_code,
#                 user = request.user
#                 )
#             serializer = BankInfoSerializer(bank_info, many=False)
#             return Response(serializer.data)
#         return Response('Bank account exist for this user, update it using put method')
        

    # def put(self, request, account_number, bank_code):
    #     if Bank_Info.objects.filter(user=request.user).exists():
    #         bank_info = Bank_Info.objects.get(user=request.user)
    #         banks = get_all_banks(request)
    #         for bank in banks:
    #             if bank_code == bank['code']:
    #                 bank_name = bank['name']
    #                 bank_code = bank['code']
    #         bank_name =bank_name
    #         bank_code = bank_code
    #         response = resolve_account_details(request, account_number, bank_code)
    #         account_name = response.get("data").get("account_name")
    #         bank_info.account_number = account_number,
    #         bank_info.account_name = account_name,
    #         bank_info.bank_name = bank_name,
    #         bank_info.bank_code = bank_code
    #         bank_info.save()
    #         serializer = BankInfoSerializer(bank_info, many=False)
    #         return Response(serializer.data)
    #     return Response('Bank account doest exist for this user, create one using post method')
        
    

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_bank_info(request):
#     if Bank_Info.objects.filter(user=request.user).exists():
#         bank_info = Bank_Info.objects.get(user=request.user)
#         bank_info.delete()
#         return Response('Bank info deleted successfully')       

                






