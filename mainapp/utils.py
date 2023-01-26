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
   
   
def send_mail_for_verify(request, user):
   current_site = get_current_site(request)
   context = {
      'user': user,
      'domain': current_site.domain,
      'uid': urlsafe_b64encode(force_bytes(user.pk)),
      'token': token.make_token(user),
   }
   message = render_to_string('mainapp/email_verify.html', context = context)
   send_mail('ITVERSE | Код подтверждения ', message, EMAIL_HOST_USER, [user.email], fail_silently=False)