from django.shortcuts import (
    render, 
    reverse 
)

from django.http import (
    HttpResponseRedirect, 
    HttpResponse
)

from users.forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def user_register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dogs:index'))

    # Создадим форму
    form = UserRegisterForm()

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            print(form.cleaned_data['password'])
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect(reverse('users:user_login'))

    context = {
        'title': 'Создать аккаунт',
        'form': form
    }

    return render(request, 'users/user_register.html', context=context)


# Loginka view
def user_login_view(request):

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(email=cleaned_data['email'], password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('dogs:index'))
            return HttpResponse("Вы либо не зарегистрированы, либо ввели неверный пароль")

    context  = {
        'title': 'Вход в аккаунт',
        'form': UserLoginForm
    }

    return render(request, 'users/user_login.html', context=context) 


# User page view
def user_profile_view(request):

    # получаем данные пользователя 
    user_object = request.user

    # проверяем полученные данные на содержимое 
    if user_object.first_name and user_object.last_name:
        user_name = user_object.first_name + ' ' + user_object.last_name
    else:
        user_name = user_object

    context = {
        'title': f'Ваш профиль {user_name}'
    }
    
    return render(request, 'users/user_profile_read_only.html', context=context)
