import secrets
from django.core.mail import send_mail
from .models import Otp
from django.contrib.auth.hashers import make_password


def generate_otp():
    return f"{secrets.randbelow(1_000_000):06d}"


def send_otp_email(user):

    otp_code = generate_otp()

    message = f'''

    سلام 🌱

    به رها خوش اومدی!

    برای تکمیل ثبت‌نام و تأیید آدرس ایمیلت، از کد زیر استفاده کن:

    کد تأیید شما:

    { otp_code }

    این کد تا ۵ دقیقه اعتبار داره و فقط یک‌بار قابل استفاده است.

    اگر شما درخواست ثبت‌نام نداده‌اید، می‌توانید این ایمیل را نادیده بگیرید.

    خوشحالیم که در مسیر مراقبت از خودت، رها رو انتخاب کردی. 💜

    با مهر،
    تیم رها

        '''

    Otp.objects.filter(
        user=user,
        is_used=False,
    ).update(is_used=True)

    Otp.objects.create(
        user=user,
        code_hash=make_password(otp_code)
    )

    send_mail(
        subject='کد تأیید ایمیل شما | رها',
        message=message,
        from_email=None,
        recipient_list=[user.email],
    )
