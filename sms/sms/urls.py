# urls.py
from django.urls import path
from .views import register_user, verify_sms_code

urlpatterns = [
    path('', register_user, name='register_user'),
    path('verify_sms_code/', verify_sms_code, name='verify_sms_code'),
    # Other paths as needed
]
