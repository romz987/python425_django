import random
import string
from django.shortcuts import (
    reverse,
    redirect
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
from django.contrib.auth.views import (
    LoginView, 
    PasswordChangeView, 
    LogoutView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.views.generic import (
    CreateView, 
    UpdateView,
    DetailView,
    ListView
)
from users.models import User
from django.urls import reverse_lazy
# Только авторизованные пользователи
from django.contrib.auth.decorators import login_required


class UserRegisterView(CreateView):

    model = User 
    form_class = UserRegisterForm 
    success_url = reverse_lazy('users:user_login')
    template_name = 'users/user_register.html'
    extra_context = {
        'title': 'Создать аккаунт',

    }

    def form_valid(self, form):
        self.object = form.save()
        send_register_email(self.object.email)
        return super().form_valid(form)


class UserLoginView(LoginView):

    form_class = UserLoginForm
    template_name = 'users/user_login.html'
    extra_context = {
        'title': 'Вход в аккаунт'
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


class UserLogoutView(LogoutView):
    template_name = 'users/user_logout.html'
    extra_context = {
        'title': 'Выход из аккаунта'
    }
    pass


class UserListView(LoginRequiredMixin, ListView):
    model = User 
    extra_context = {
        'title': 'Питомник - все наши пользователи'
    }
    template_name = 'users/users.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class UserDetailView(DetailView):
    model = User 
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        user_obj = context_data['object']
        context_data['title'] = f'Профиль пользователя {user_obj}'    
        return context_data


# User logout view 
@login_required(login_url='users:user_login')
def user_generate_new_password_view(request):
    new_password = ''.join(
        random.sample(string.ascii_letters + string.digits, 12)
    )
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
