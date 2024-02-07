# forms.py
from django import forms

class UserInfoForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='Ismingiz')
    last_name = forms.CharField(max_length=100, label='Familiyangiz')
    phone_number = forms.CharField(max_length=15, label='Telefon raqamingiz', help_text='Masalan: +998901234567')

class SMSVerificationForm(forms.Form):
    sms_code = forms.CharField(max_length=6, min_length=6, label='SMS Kod', widget=forms.TextInput(attrs={'class': 'form-control'}))
