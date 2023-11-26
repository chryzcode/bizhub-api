from django.urls import path
from .views import *

urlpatterns = [
    path('create/<client_id>/', create_order, name='create_order'),
    path('filter/<client_id>/', filter_buiness_orders, name='filter_buiness_orders'),
    path('delete/<order_id>/', delete_order, name='delete_order'),
    path('get/<order_id>/', get_order, name='get_order'),
    path('business-orders/', get_buiness_orders, name='get_buiness_orders'),
    path('unpaid/', get_unpaid_buiness_orders, name='get_unpaid_buiness_orders'),
    path('paid/', get_paid_buiness_orders, name='get_paid_buiness_orders'),
]
