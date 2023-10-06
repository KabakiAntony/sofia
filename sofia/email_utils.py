import logging
from django.contrib import messages
from django.core.mail import EmailMessage
from smtplib import SMTPAuthenticationError, SMTPException
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.urls import reverse

from sofia.tokens import account_activation_token, password_reset_token

logger = logging.getLogger(__name__)


def _send_email(request, receiver_email, the_subject, the_content):
    try:
        msg = EmailMessage(
            the_subject,
            the_content,
            "Sofia <noreply@sofia.co.ke>",
            [receiver_email])
        msg.content_subtype = "html"
        msg.send()

    except SMTPAuthenticationError as e:
        logger.error(f"SMTPAuthenticationError: {e}")
        messages.add_message(request, messages.ERROR,
                             "An error occured while sending email, the admin has been notified.")

    except SMTPException as e:
        logger.error(f"SMTP Error: {e}")
        messages.add_message(request, messages.ERROR,
                             "An error occured while sending email, the admin has been notified.")

    except Exception as e:
        return messages.add_message(request, messages.ERROR,
                                    f"An error occured while sending emails, the admin has been notified. {e}")


def send_verification_email(request, user, email):
    current_site = get_current_site(request)
    protocol = request.scheme
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    activation_url = reverse('verify', kwargs={'uidb64': uid, 'token': token})
    activation_link = f"{protocol}://{current_site.domain}{activation_url}"

    subject = "Welcome and verify your email"
    content = render_to_string("accounts/verify_email_body.html", {
        'user': user,
        'current_site': current_site,
        'activation_link': activation_link
    })

    _send_email(request, email, subject, content)


def send_password_reset_email(request, user, email):
    current_site = get_current_site(request)
    protocol = request.scheme
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)

    reset_url = reverse('change', kwargs={'uidb64': uid, 'token': token})
    reset_link = f"{protocol}://{current_site.domain}{reset_url}"
    print(reset_link)
    subject = " Password reset link."
    content = render_to_string("accounts/password_reset_req_email_body.html", {
        'user': user,
        'current_site': current_site,
        'reset_link': reset_link
    })

    _send_email(request, email, subject, content)
