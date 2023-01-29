from mainapp.forms import UserRegistration, UserAuthentication, UserPasswordReset

def get_context_data(request):
   context = {
      'log_ajax': UserAuthentication(),
      'reg_ajax': UserRegistration(),
      'reset_ajax': UserPasswordReset(),
   }
   return context