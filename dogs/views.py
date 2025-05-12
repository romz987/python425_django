from django.template.context_processors import request
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

# My imports
from dogs.models import Breed, Dog, DogParent
from dogs.forms import DogForm, DogParentForm, DogAdminForm
from dogs.services import send_views_email
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from users.models import UserRoles

# Только авторизованные пользователи
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

# For CBV
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    ListView,
)


class IndexView(ListView):
    model = Breed
    template_name = "dogs/index.html"
    context_object_name = "objects_list"

    def get_queryset(self):
        return Breed.objects.all()[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Питомник - Главная страница"
        return context


class BreedListView(ListView):
    model = Breed
    extra_context = {"title": "Все наши породы"}
    template_name = "dogs/breeds.html"


class DogBreedListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = "dogs/dogs.html"
    extra_context = {"title": "Собаки выбранной породы"}

    def get_queryset(self):
        queryset = super().get_queryset().filter(breed_id=self.kwargs.get("pk"))
        return queryset


class DogListView(ListView):
    model = Dog
    template_name = "dogs/dogs.html"
    context_object_name = "objects_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Все наши собаки"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivatedListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = "dogs/dogs.html"
    context_object_name = "objects_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Все наши собаки"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogCreateView(LoginRequiredMixin, CreateView):
    # Модель базы данных
    model = Dog
    form_class = DogForm
    template_name = "dogs/create.html"
    success_url = reverse_lazy("dogs:dogs_list")
    login_url = reverse_lazy("users:user_login")

    def form_valid(self, form):
        # form.instanc.owner = self.request.user
        # return super().form_valid(form)
        if self.request.user.role != UserRoles.USER:
            raise PermissionDenied()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = "dogs/detail.html"
    context_object_name = "object"
    login_url = reverse_lazy("users:user_login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog = self.get_object()
        context["title"] = f"{dog.name} - {dog.breed.name}"
        # информация о родителях
        context["parents"] = DogParent.objects.filter(dog=self.object)
        object_ = context["object"]
        dog_object_increase = get_object_or_404(Dog, pk=object_.pk)
        if object_.owner != self.request.user and self.request.user.role not in [
            UserRoles.ADMIN,
            UserRoles.MODERATOR,
        ]:
            dog_object_increase.views_count()
        if object_.owner:
            object_owner_email = object_.owner.email
            # Email отправляется при каждом просмотре для удобства
            if dog_object_increase.views % 20 == 0 and dog_object_increase.views != 0:
                send_views_email(
                    dog_object_increase.name,
                    object_owner_email,
                    dog_object_increase.views,
                )
        return context


class DogUpdateView(LoginRequiredMixin, UpdateView):
    # Укажем, с какой моделью и формой работает CBV
    model = Dog
    # Укажем, что должна использоваться пользовательская форма
    # вместо формы по умолчанию
    form_class = DogForm
    # Укажем используемый шаблон
    template_name = "dogs/update.html"
    # Если пользователь не авторизован, то он отправится на
    # этот url
    login_url = reverse_lazy("user:user_login")

    # Куда отправим пользователя после успешного сохранения формы
    def get_success_url(self):
        return reverse_lazy("dogs:dog_detail", kwargs={"pk": self.object.pk})

    # Как получить редактируемый объект
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        print("1. Объект ДО формы:", self.object.birth_date)
        if (
            self.object.owner != self.request.user
            and self.request.user.role != UserRoles.ADMIN
        ):
            raise PermissionDenied()
        return self.object

    
    def get_form_class(self):
        dog_forms = {
            UserRoles.ADMIN: DogAdminForm,
            UserRoles.MODERATOR: DogForm,
            UserRoles.USER: DogForm
        }
        user_role = self.request.user.role
        dog_form_class = dog_forms[user_role]
        return dog_form_class


    # Дополняет контекст шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print("2. Объект ПОСЛЕ формы:", self.object.birth_date)
        # print("Form initial data:", context['form'].initial)
        # print("Form instance data:", vars(context['form'].instance))
        DogParentFormset = inlineformset_factory(
            Dog, DogParent, form=DogParentForm, extra=2
        )
        if self.request.method == "POST":
            formset = DogParentFormset(self.request.POST, instance=self.object)
        else:
            formset = DogParentFormset(instance=self.object)
        context["title"] = f"Изменить собаку {self.object}"
        context["formset"] = formset
        return context

    # Выполняется, если основная форма прошла валидацию
    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class DogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Dog
    template_name = "dogs/delete.html"
    context_object_name = "object"
    login_url = "users:user_login"
    success_url = reverse_lazy("dogs:dogs_list")
    permission_required = "dogs.delete_dog"
    permission_denied_message = "У вас нет для данного действия"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удалить собаку"
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


def dog_toggle_activity(request, pk):
    """Переключение активности для собаки"""
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse("dogs:dogs_list"))
