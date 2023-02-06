from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator as gtoken
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import FormMixin, FormView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from base64 import urlsafe_b64decode
from .forms import *
from .models import *
from .utils import *

# main page
class HomePage(ListView, FormMixin):
    model = get_user_model()
    form_class = UserAuthentication
    context_object_name = 'posts'
    template_name = 'mainapp/index.html'
    success_url = reverse_lazy('home')
    
    def get_queryset(self):
        return articles.objects.filter(is_published=True).order_by('-time_create')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def post(self, request, *args, **kwargs):
        #authorization
        if len(request.POST) == 3:
            self.form = self.get_form()
            if self.form.is_valid():
                username = self.form.cleaned_data.get('username')
                password = self.form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None and user.email_verify == True:
                    login(request, user)
                    return JsonResponse(data={}, status=201)
                else:
                    return JsonResponse(data={'errors':{'email': 'Аккаунт не активен!'}}, status=400)
            else:
                return JsonResponse(data={'errors': self.form.errors, }, status=400)
        
        #registration
        elif len(request.POST) == 5:
            self.form_class = UserRegistration
            self.form = self.get_form()
            if self.form.is_valid():
                self.object = self.form.save()
                mail = self.form.cleaned_data.get('email')
                self.object.email = mail.lower()
                self.object.save()
                send_mail_for_verify(request, self.object)
                return JsonResponse(data={}, status=201)
            else:
                return JsonResponse(data={'errors': self.form.errors,}, status=400)
           
        #restoring account access
        elif len(request.POST) == 2:
            self.form_class = PasswordResetForm
            self.form = self.get_form()
            if self.form.is_valid():
                data = self.form.cleaned_data.get('email').lower()
                try:
                    user = MyUser.objects.get(email = data)
                    send_mail_for_reset(request, user)
                    return JsonResponse(data={}, status=201)
                except:
                    return JsonResponse(data={'errors': {'email': 'Аккаунт не найден!'}}, status=400)
            else:
                return JsonResponse(data={'errors': {'email': 'Некорректный email адрес!'}}, status=400)
            
        else:
            return HttpResponse('error')
    

class economy(ListView):
    template_name = 'mainapp/economy.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Экономика'}
    
    # отбор записей в раздел экономика
    def get_queryset(self):
        return articles.objects.filter(is_published=True, section='economy').order_by('-time_create')
    
class dev(ListView):
    template_name = 'mainapp/dev.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Разработка | IT'}
    
    # отбор записей в раздел экономика
    def get_queryset(self):
        return articles.objects.filter(is_published=True, section='dev').order_by('-time_create')
    
class life(ListView):
    template_name = 'mainapp/dev.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Жизнь'}
    
    # отбор записей в раздел экономика
    def get_queryset(self):
        return articles.objects.filter(is_published=True, section='life').order_by('-time_create')


# отображение статьи на её странице + comments
class ShowArticle(FormMixin, DetailView):
    model = articles
    form_class = AddCommentForm
    template_name = 'mainapp/article.html'
    slug_url_kwarg = 'post_slug'  # своя переменная для слага
    context_object_name = 'post'  # html
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShowArticle, self).get_context_data(**kwargs)    #получаем сформированный контекст
        context['comments'] = context['post'].cmnts.filter(is_active=True)
        #context['answers'] = context['post'].answs.filter(is_active=True)
        context['likes'] = context['post'].likes.filter(like=True)
        context['title'] = self.object.title
        context['answer'] = AddAnswerForm(self.request.POST)
        return context
     
    # перенаправление на эту же страницу (исправить)
    def get_success_url(self, **kwargs):
        return reverse_lazy('article', kwargs={'post_slug': self.get_object().slug, 'section_slug':self.get_object().section})
    
    # переопределение метода для обработки post запроса
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                if 'parent' in request.POST:
                    _parent = get_object_or_404(comments, id = request.POST['parent'])
                else:
                    _parent = None
            except:
                _parent = None
            return self.form_valid(form, _parent)
        else:
            return self.form_invalid(form)

    # сохранение формы в БД
    def form_valid(self, form, _parent):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = self.get_object()
        self.object.parent = _parent
        self.object.save()
        return super().form_valid(form)
   
    
class userpage(DetailView):
    model = get_user_model()
    template_name = 'mainapp/p.html'
    slug_url_kwarg = 'username'
    slug_field = 'userslug' # The name of the field on the model that contains the slug. By default, slug_field is 'slug'.
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)    #получаем сформированный контекст
        user = get_object_or_404(get_user_model(), userslug=self.kwargs['username'])
        context['thisuser'] = user
        context['title'] = 'ITVERSE — ' + user.username
        return context
    

class userpagesettings(DetailView):
    model = get_user_model()
    template_name = 'mainapp/psettings.html'
    slug_url_kwarg = 'username'
    slug_field = 'userslug'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)    #получаем сформированный контекст
        context['thisuser'] = get_object_or_404(get_user_model(), userslug=self.kwargs['username'])
        context['title'] = 'Настройки пользователя'
        return context

class EmailVerify(LoginView):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and gtoken.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            return HttpResponse('error registration')
    
    def get_user(self, uidb64):
        try:
            uid = urlsafe_b64decode(uidb64[1::]).decode()
            user = MyUser.objects.get(pk = uid)
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist, forms.ValidationError):
            user = None
        return user

INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"

class PasswordResetConfirm(FormView):
    form_class = UserPasswordSet
    success_url = reverse_lazy("home")
    template_name = "mainapp/password_reset_confirm.html"
    reset_url_token = "set-password"
    
    def dispatch(self, *args, **kwargs):
        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])
        
        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if gtoken.check_token(self.user, session_token):
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            
            else:
                if gtoken.check_token(self.user, token):
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)    
        
        return HttpResponse('reset error')
    
    def get_user(self, uidb64):
        try:
            uid = urlsafe_b64decode(uidb64[1::]).decode()   
            user = MyUser.objects.get(pk = uid)
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist, forms.ValidationError):
            user = None
        return user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user 
        return kwargs
    
    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)

    
# обработка исключения при несовпадении шаблона
def PageNotFound(request, exception):
    return render(request, 'mainapp/error.html')

# выход
def logout_user(request):
    logout(request)
    return redirect('/')