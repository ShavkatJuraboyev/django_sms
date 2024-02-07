# views.py
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserInfoForm, SMSVerificationForm
from .models import UserProfile 
from django.conf import settings
import http.client

def send_sms_to_user(phone_number, sms_code):
    url = settings.BASE_URL
    token = settings.API_KEY
    SENDER = settings.SENDER
    RECIPIENT = f"{phone_number}"
    print(f'SMS code sent to {phone_number}: {sms_code}')
    MESSAGE_TEXT = f"Sizni arizani tasdiqlash kodingiz: {sms_code}"

    conn = http.client.HTTPSConnection(url)

    payload1 = "{\"messages\":" \
               "[{\"from\":\"" + SENDER + "\"" \
                                          ",\"destinations\":" \
                                          "[{\"to\":\"" + RECIPIENT + "\"}]," \
                                                                      "\"text\":\"" + MESSAGE_TEXT + "\"}]}"

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn.request("POST", "/sms/2/text/advanced", payload1, headers)

def register_user(request):
    if request.method == 'POST':
        user_info_form = UserInfoForm(request.POST)
        if user_info_form.is_valid():
            # Generate and send SMS code
            sms_code = str(random.randint(100000, 999999))
            send_sms_to_user(request.POST['phone_number'], sms_code)

            # Save user info and SMS code in session
            request.session['user_info'] = {
                'first_name': user_info_form.cleaned_data['first_name'],
                'last_name': user_info_form.cleaned_data['last_name'],
                'phone_number': user_info_form.cleaned_data['phone_number'],
                'sms_code': sms_code,
            }

            return redirect('verify_sms_code')
    else:
        user_info_form = UserInfoForm()

    context = {'user_info_form': user_info_form}
    return render(request, 'register_user.html', context)

def verify_sms_code(request):
    if request.method == 'POST':
        sms_verification_form = SMSVerificationForm(request.POST)
        if sms_verification_form.is_valid():
            user_info = request.session.get('user_info')
            print('user_info:', user_info)
            if user_info and request.POST['sms_code'] == user_info['sms_code']:
                # Save user information to the database
                UserProfile.objects.create(
                    first_name=user_info['first_name'],
                    last_name=user_info['last_name'],
                    phone_number=user_info['phone_number']
                )

                # Clear session data
                request.session.pop('user_info')

            return redirect('register_user')
    else:
        sms_verification_form = SMSVerificationForm()
    context = {'sms_verification_form': sms_verification_form}
    return render(request, 'verify_sms_code.html', context)
