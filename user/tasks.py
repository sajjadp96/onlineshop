from celery import shared_task
from django.core.mail import send_mail
from config import settings
from user.utils import get_all_users_email,ad_message


@shared_task(bind=True)
def send_notification_mail(self, target_mail, message):
    mail_subject = "SajiShope"
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[target_mail],
        fail_silently=False,
        )
    return "Done"



@shared_task(bind=True)
def send_ad_mails(self):
    # recipient_list = ["sajjad.piri1997@gmail.com"]
    mail_subject = "Sajishop"
    send_mail(
        subject = mail_subject,
        message=ad_message(),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=get_all_users_email(),
        fail_silently=False,
        )
    return "Done"



@shared_task(bind=True)
def send_otp_mail(self, target_mail, message):
    mail_subject = "SajiShope"
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[target_mail],
        fail_silently=False,
        )
    return "Done"