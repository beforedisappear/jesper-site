from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import *

class AddArticleForm(forms.ModelForm):
   #констуктор для невыбранного значения формы
   def __init__(self, *args, **kwargs):
      super(AddArticleForm, self).__init__(*args, **kwargs)
      #self.fields['section'].empty_label = ' '
      self.fields["section"].choices = [("", ""),] + list(self.fields["section"].choices)[1:]
   
   class Meta:
      #связь формы с моделью
      model = articles
      #отображаемые поля
      fields = ['section', 'author', 'title', 'subtitle', 'text', 'content']
      widgets = {
         'title': forms.TextInput(attrs={"class": "form-input"}),
         'text': forms.Textarea(attrs={"cols": 60, "rows": 10}),
      }
      
class AddCommentForm(forms.ModelForm):
   class Meta:
      model = comments
      fields = ['text']
      widgets = {
         'text': forms.Textarea(attrs={"class": "form-control", "placeholder": "Add your comment here", 
                                       "rows": "3", "cols": "61", "style":"resize:none;", }),
      }
      labels = {
        'text': '',
      }
      
class AddAnswerForm(AddCommentForm):
   
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #print(self.fields['parent'])                    
        
   class Meta:
      model = comments
      fields = ['text', 'parent']
      widgets = {
         'text': forms.Textarea(attrs={"class": "cmt-form", "placeholder": "Add your comment here", 
                                       "rows": "3", "cols": "61", "style":"resize:none;",}),
      }
      
      
class UserRegistration(UserCreationForm):
   
   password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "text-field__input"}))
   password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={"class": "text-field__input"}),)
      
   def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

   def clean(self):
      email = self.cleaned_data.get('email')
      if email is not None and MyUser.objects.filter(email=email.lower()).exists():
         raise ValidationError("Данный Email уже занят!")
      return self.cleaned_data
        
   class Meta(UserCreationForm.Meta):
      model = get_user_model()
      fields = ['email', 'username', 'password1']
      widgets = {'email': forms.TextInput(attrs={"class": "text-field__input"}),
                 'username': forms.TextInput(attrs={"class": "text-field__input"}),
      }
      
class UserAuthentication(AuthenticationForm):
   # email = username
   def clean(self):
      data = self.data.copy()
      data['username'] = data['username'].lower()
      return data
   
class UserPasswordReset(PasswordResetForm):
   pass