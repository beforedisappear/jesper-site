# additional support files (mixins storage)
from django.contrib.auth.tokens import default_token_generator as token
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from base64 import urlsafe_b64encode
from jespersite.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string


class DataMixin:
   def get_user_context(self, **kwargs):
      context = kwargs
      return context 


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/user_<username>/<filename>
    return 'users/user_{0}/{1}'.format(instance.username, filename)
   
   
def send_mail_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
      'user': user,
      'domain': current_site.domain,
      'uid': urlsafe_b64encode(force_bytes(user.pk)),
      'token': token.make_token(user),
    }
    message = render_to_string('mainapp/email_verify.html', context = context)
    send_mail('ITVERSE | Код подтверждения', message, EMAIL_HOST_USER, [user.email], fail_silently=False)
   

def send_mail_for_reset(request, user):
    current_site = get_current_site(request)
    context = {
      'domain': current_site.domain,
      'uid': urlsafe_b64encode(force_bytes(user.pk)),
      'token': token.make_token(user),
    }
    message = render_to_string('mainapp/email_password_reset.html', context = context)
    send_mail('ITVERSE | Восстановление доступа', message, EMAIL_HOST_USER, [user.email], fail_silently=False)
 
 
def correct_email(email):
    email = email or ""
    try:
        email_name, domain_part = email.strip().rsplit("@", 1)
    except ValueError:
        pass
    else:
        email = email_name.lower() + "@" + domain_part.lower()
    return email