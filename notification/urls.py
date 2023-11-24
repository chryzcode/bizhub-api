from django.urls import path
from .views import *

urlpatterns = [
    path('get/<notification_id>/', get_notification_details, name="get_notification_details"),
    path('', get_all_notifications, name="get_all_notifications"),
    path('get-unread/', get_unread_notifications, name="get_unread_notifications"),
    path('get-read/', get_read_notifications, name="get_read_notifications"),
    path('mark-as-read/<notification_id>/', mark_notification_as_read, name="mark_notification_as_read"),
]
