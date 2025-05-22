from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from foodonline import settings
def detectuser(user):
    if user.role == 1:
        return 'vendorDashboard'  # Must match the URL name in urls.py
    elif user.role == 2:
        return 'customerDashboard'
    elif user.role is None and user.is_superadmin:
        return 'admin'
    return 'home'  # Default fallback
def send_verification_email(request,user,mail_subject,email_template):
    from_email=settings.DEFAULT_FROM_EMAIL
    current_site=get_current_site(request)
     
    message=render_to_string(email_template,{'user':user,
                                                                             'domain':current_site,
                                                                             'uid':urlsafe_base64_decode(force_bytes(user.pk)),
                                                                             'token': default_token_generator.make_token(user),})
    to_email=user.email
    mail=EmailMessage(mail_subject,message,to=[to_email])
    mail.send()
 