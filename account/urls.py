from django.urls import path
from .views import *

urlpatterns = [
    path('all-users/', all_users, name="all_users"),
    path('a_user/<slugified_business_name>/', a_user, name="a_user"),
    path('current-user/', current_user, name="current_user"),
    path('login/', account_login, name="account_login"),
    path('logout/', account_logout, name="account_logout"),
    path('register/', account_register, name="account_register"),
    path('update/', account_update, name="acccount_update"),
    path('logout/', account_delete, name="account_logout"),
    # path('get-all-banks/', get_all_banks, name='get_all_banks'),
    # path('resolve-account-details/', resolve_account_details, name='resolve_account_details'),
    # path('user-account-bank/<account_number>/<bank_code>/', user_account_bank.as_view(), name='user_account_bank'), 
    # path('delete-bank-info/', delete_bank_info, name='delete_bank_info'),  
]
