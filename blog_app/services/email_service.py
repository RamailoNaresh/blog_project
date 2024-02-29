from django.core.mail import send_mail
from random import randint
from django.utils import timezone
from django.conf import settings
from blog_app.ForgetPassword.serializers import ForgetPasswordSerializer
from blog_app.util.util import get_char_uuid

def send_otp_mail(author):
    generated_otp = "".join([str(randint(0,9)) for _ in range(0, 6) ])
    author.otp = generated_otp
    author.otp_sent_date = timezone.now()
    author.save()
    send_mail(
        "OTP Varification",
        f"Your otp for verification is {generated_otp}. Please verify as soon as possible. OTP is valid for 10 minutes only.",
        "tamangnaresh386@gmail.com",
        [author.email],
        fail_silently=True
    )



def send_forget_password_link(author):
    uuid = get_char_uuid()
    data ={
            "token": uuid,
            "author": author.id
        }
    obj = ForgetPasswordSerializer(data = data)
    if obj.is_valid():
        obj.save()
        send_mail(
            "Forget Password",
            f"Please click on the link below to set new password. \n http://127.0.0.1:8000/v1/forget_password/{uuid}/",
            "tamangnaresh386@gmail.com",
            [author.email],
            fail_silently=True
        )
        return True
    return obj.errors