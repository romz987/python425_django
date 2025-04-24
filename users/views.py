import random
import string
from django.shortcuts import (
    render, 
    reverse,
    redirect
)

from django.http import (
    HttpResponseRedirect, 
    HttpResponse
)

from users.forms import (
    UserRegisterForm, 
    UserLoginForm,
    UserUpdateForm,
    UserChangePasswordForm,
    UserForm
)

from users.services import (
    send_register_email, 
    send_new_password
)

from django.contrib.auth import (
    authenticate, 
    login, 
    logout,
    update_session_auth_hash
)

from django.contrib.auth.views import (
    LoginView, 
    PasswordChangeView, 
    LogoutView
)

from django.views.generic import (
    CreateView, 
    UpdateView
)

from users.models import User
from django.urls import reverse_lazy
# Только авторизованные пользователи
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class UserRegisterView(CreateView):

    model = User 
    form_class = UserRegisterForm 
    success_url = reverse_lazy('users:user_login')
    template_name = 'users/user_register.html'
    extra_context = {
        'title': 'Создать аккаунт',

    }


class UserLoginView(LoginView):

    form_class = UserLoginForm
    template_name = 'users/user_login.html'
    extra_context = {
        'title':'Вход в аккаунт'
    }


class UserProfileView(UpdateView):
    model = User 
    form_class = UserForm 
    template_name = 'users/user_profile_read_only.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = f'Ваш профиль {self.get_object()}'
        return context_data


class UserUpdateView(UpdateView):
    model = User 
    form_class = UserUpdateForm 
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = f'Обновить профиль {self.get_object()}'
        return context_data


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserChangePasswordForm
    template_name = 'users/user_change_password.html'
    success_url = reverse_lazy('users:user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = f'Изменить пароль {self.request.user}'
        return context_data


@login_required(login_url='users:user_login')
def user_update_view(request):
    user_object = request.user
    if request.method == 'POST':
        form = UserUpdateForm(
            request.POST, 
            request.FILES, 
            instance=user_object
        )
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return HttpResponseRedirect(reverse('users:user_profile'))
    context = {
        'object': user_object,
        'title': (
            f'Изменить профиль {user_object.email} '
            #f'{user_object.last_name}'
        ),
        'form': UserUpdateForm(instance=user_object)
    }
    return render(request, 'users/user_update.html', context=context)


# User logout view 
@login_required(login_url='users:user_login')
def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')


# User logout view 
@login_required(login_url='users:user_login')
def user_generate_new_password_view(request):
    new_password = ''.join(random.sample(string.ascii_letters + string.digits, 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))


# Create your views here.
# def user_register_view(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('dogs:index'))
#
#     # Создадим форму
#     form = UserRegisterForm()
#
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             print(new_user)
#             print(form.cleaned_data['password'])
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()
#             send_register_email(new_user.email)
#             return HttpResponseRedirect(reverse('users:user_login'))
#
#     context = {
#         'title': 'Создать аккаунт',
#         'form': form
#     }
#
#     return render(request, 'users/user_register.html', context=context)


# Loginka view
# def user_login_view(request):
#
#     if request.method == "POST":
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             user = authenticate(
#                 email=cleaned_data['email'], password=cleaned_data['password']
#             )
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponseRedirect(reverse('dogs:index'))
#             return HttpResponse(
#                 "Вы либо не зарегистрированы, либо ввели неверный пароль"
#             )
#
#     context  = {
#         'title': 'Вход в аккаунт',
#         'form': UserLoginForm
#     }
#
#     return render(request, 'users/user_login.html', context=context) 


# # Смена пароля пользователя
# @login_required(login_url='users:user_login')
# def user_change_password_view(request):
#     user_object = request.user 
#     form = UserChangePasswordForm(user_object, request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             user_object = form.save()
#             update_session_auth_hash(request, user_object)
#             messages.success(request, 'Пароль был успешно изменен')
#             return HttpResponseRedirect(reverse('users:user_profile'))
#         else:
#             messages.error(request, 'Не удалось изменить пароль')
#     context = {
#         'title': (
#             f'Изменить пароль {user_object.first_name} '
#             f'{user_object.last_name}'
#         ),
#         'form': form 
#     }
#     return render(request, 'users/user_change_password.html', context=context)


# # User page view
# @login_required(login_url='users:user_login')
# def user_profile_view(request):
#
#     # получаем данные пользователя 
#     user_object = request.user
#
#     # проверяем полученные данные на содержимое 
#     if user_object.first_name and user_object.last_name:
#         user_name = user_object.first_name + ' ' + user_object.last_name
#     else:
#         user_name = user_object
#
#     context = {
#         'title': f'Ваш профиль {user_name}'
#     }
#     
#     return render(
#         request, 
#         'users/user_profile_read_only.html', 
#         context=context
#     )


