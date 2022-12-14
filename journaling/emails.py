from django.contrib import messages
from django.core.mail import EmailMessage

def _send_email(request, receiver_email, the_subject, the_content):
    try:
        msg = EmailMessage(
            the_subject,
            the_content,
            "Journaling Therapy <noreply@journalingtherapy.co.ke>",
            [receiver_email])
        msg.content_subtype = "html"
        msg.send()
    except Exception as e:
        return messages.error(request, f"Error occured sending mail, {e}")
    