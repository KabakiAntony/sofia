import os
from django.core.mail import EmailMessage
from django.contrib import messages
from journaling.settings import env

def send_email(request, receiver_email, the_subject, the_content):
    """send email on relevant user action"""
    if receiver_email and the_subject and the_content:
        try:
            subject, from_email, to = the_subject, env('FROM_EMAIL'), receiver_email
            html_content = the_content
            message = EmailMessage(subject, html_content, from_email, [to])
            message.content_subtype = "html"
            message.send()
        except Exception as e:
            return messages.error(request, f"The following error occured, {e}")
