# tasks.py (inside your Django app)
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email, user):
    subject = f'Welcome {user} to Chat App'
    message = 'Thank you for registering with Chat App. We are excited to have you on board!'
    from_email = settings.DEFAULT_FROM_EMAIL 

    # Send the email asynchronously
    send_mail(subject, message, from_email, [user_email])
