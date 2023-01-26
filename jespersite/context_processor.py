from mainapp.forms import UserRegistration, AuthenticationForm

def get_context_data(request):
   context = {
      'log_ajax': AuthenticationForm(),
      'reg_ajax': UserRegistration(),
   }
   
   return context