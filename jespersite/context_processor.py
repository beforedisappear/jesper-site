from mainapp.forms import *

def get_context_data(request):
   context = {
      'log_ajax': UserAuthentication(),
      'reg_ajax': UserRegistration(),
      'reset_ajax': UserPasswordReset(),
      #'confirm_ajax': UserPasswordSet(),
   }
   return context