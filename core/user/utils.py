from kavenegar import KavenegarAPI
import random

def generate_otp(length=6):
    for _ in range(length):
        otp = str(random.randint(0, 9))

    return otp

def send_otp(phone_num, otp):
    api_key = KavenegarAPI('')  # Enter your API key here.
    payload = {
        'sender' : '',  # Enter your sender code here.
        'receptor': phone_num,
        'message' :f'Your verification code: {otp}'
    }
    response = api_key.sms_send(payload)
    print(response)
