from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_client, name='create_client'),
    path('update/<client_id>/', update_client, name='update_client'),
    path('get/<client_id>/', get_client, name='get_client'),
    path('all-clients/', get_business_clients, name='get_business_clients'),
    path('delete/<client_id>', delete_client, name='delete_client'),
]
