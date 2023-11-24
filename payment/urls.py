from django.urls import path
from.views import *

urlpatterns = [
    path("initiate/<uuid:pk>/", initiate_payment, name="initiate_payment"),
    path("verify/<ref>/", verify_payment, name="verify_payment"),
    path('<payment_id>/', get_payment, name='get_payment'),
    path('business-payments/', get_buiness_payments, name='get_buiness_payments'),
    path('filter/<client_id>/', filter_client_payments, name='filter_client_payments'),
]
