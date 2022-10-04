from django.contrib import messages
from journaling.settings import env
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(request, receiver_email, the_subject, the_content):
    """send email on relevant user action"""
    message = Mail(
        from_email=(env('FROM_EMAIL'), "Journaling Therapy"),
        to_emails=receiver_email,
        subject=the_subject,
        html_content=the_content,
    )
    try:
        sg = SendGridAPIClient(env("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
            return messages.error(request, f"The following error occured, {e}")