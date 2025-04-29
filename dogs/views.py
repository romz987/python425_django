from django.template.context_processors import request
from django.shortcuts import render, get_object_or_404 
from django.http import Http404

# My imports 
from dogs.models import Breed, Dog, DogParent
from dogs.forms import DogForm, DogParentForm
from django.http import HttpResponseRedirect 
from django.urls import reverse, reverse_lazy  
from django.forms import inlineformset_factory

# Только авторизованные пользователи 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# For CBV 
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    ListView
)


class IndexView(ListView):
    model = Breed
    template_name = 'dogs/index.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return Breed.objects.all()[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Питомник - Главная страница'
        return context


class BreedsListView(ListView):
    model = Breed
    template_name = 'dogs/breeds.html'
    context_object_name = 'objects_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Питомник - Все наши породы'
        return context


class BreedDogsListView(ListView):
    model = Dog
    template_name = 'dogs/dogs.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return Dog.objects.filter(breed_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breed_object = Breed.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Собаки породы - {breed_object}'
        context['breed_pk'] = breed_object.pk
        return context


class DogListView(ListView):
    model = Dog 
    template_name = 'dogs/dogs.html'
    context_object_name = 'objects_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все наши собаки'
        return context


# CRUD
class DogCreateView(LoginRequiredMixin, CreateView):
    # Модель базы данных
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:dogs_list')
    login_url = reverse_lazy('users:user_login')

    def form_valid(self, form):
        # form.instanc.owner = self.request.user 
        # return super().form_valid(form)
        self.object = form.save()
        self.object.owner = self.request.user 
        self.object.save()
        return super().form_valid(form)


class DogDetailView(LoginRequiredMixin, DetailView):
    model = Dog 
    template_name = 'dogs/detail.html'
    context_object_name = 'object'
    login_url = reverse_lazy('users:user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog = self.get_object()
        context['title'] = f'{dog.name} - {dog.breed.name}'
        # информация о родителях
        context['parents'] = DogParent.objects.filter(dog=self.object)
        return context


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog 
    form_class = DogForm 
    template_name = 'dogs/create_update.html'
    login_url = reverse_lazy('user:user_login')

    def get_success_url(self):
        return reverse_lazy(
            'dogs:dog_detail',
            kwargs={'pk':self.object.pk}
        )

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (self.object.owner != self.request.user 
                and not self.request.user.is_staff):
            raise Http404
        return self.object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DogParentFormset = inlineformset_factory(
            Dog, 
            DogParent,
            form = DogParentForm,
            extra=1
        )
        if self.request.method == "POST":
            formset = DogParentFormset(self.request.POST, instance=self.object)
        else:
            formset = DogParentFormset(instance=self.object)
        object_ = self.get_object()
        context['title'] = f'Изменить собаку {object_}'
        context['formset'] = formset
        return context

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object 
            formset.save()
        return super().form_valid(form)


class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog  
    template_name = 'dogs/delete.html'
    context_object_name = 'object'
    login_url = 'users:user_login'
    success_url = reverse_lazy('dogs:dogs_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить собаку'
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


# @login_required(login_url='users:user_login')
# def dog_delete_view(request, pk):
#     """ Удалить собаку """
#     dog_object = get_object_or_404(Dog, pk=pk)
#     if request.method == 'POST':
#         dog_object.delete()
#         return HttpResponseRedirect(reverse('dogs:dogs_list'))
#     context = {
#         'object': dog_object,
#         'title': 'Удалить собаку'
#     }
#     return render(request, 'dogs/delete.html', context=context)


# CRUD 
# def dog_create_view(request):
#     """ Для создания нового объекта и помещения его в базу """
#     if request.method == 'POST':
#         form = DogForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('dogs:dogs_list'))
#     context = {
#         'title': 'Добавить собаку',
#         'form': DogForm
#     }
#     return render(request, 'dogs/create.html', context=context)


# @login_required(login_url='users:user_login')
# def dog_create_view(request):
#     """ Создать собаку """
#     if request.method == 'POST':
#         form = DogForm(request.POST, request.FILES)
#         if form.is_valid():
#             dog_object = form.save()
#             dog_object.owner = request.user 
#             dog_object.save()
#             #form.save()
#             return HttpResponseRedirect(reverse('dogs:dogs_list'))
#         else:
#             print(form.errors)  # Добавьте эту строку для отладки
#     else:
#         form = DogForm()
#
#     context = {
#         'title': 'Добавить собаку',
#         'form': form
#     }
#     return render(request, 'dogs/create_update.html', context=context)


# @login_required(login_url='users:user_login')
# def dog_detail_view(request, pk):
#     """ Вернуть детальную информацию о собаке """
#     dog_object = Dog.objects.get(pk=pk)
#     context = {
#         'object': dog_object,
#         'title': dog_object.name + ' - ' + dog_object.breed.name
#     }
#     return render(request, 'dogs/detail.html', context=context)


# def dog_list_view(request):
#     context = {
#         'objects_list': Dog.objects.all(),
#         'title': f'Все наши собаки',
#     }   
#     return render(request, 'dogs/dogs.html', context)


# # отображение всех объектов независимо от модели 
# def breeds_list_view(request):
#     context = {
#         'objects_list': Breed.objects.all(),
#         'title': 'Питомник - Все наши породы'
#     }
#     return render(request, 'dogs/breeds.html', context=context)


#
# # Create your views here.
# def index_view(request):
#     context = {        
#         'objects_list': Breed.objects.all()[:3],
#         'title': 'Питомник - Главная страница'
#     }
#     return render(request, 'dogs/index.html', context=context)


# def breed_dogs_list_view(request, pk: int):
#     breed_object = Breed.objects.get(pk=pk)
#     context = {
#         'objects_list': Dog.objects.filter(breed_id=pk),
#         'title': f'Собаки породы - {breed_object}',
#         'breed_pk': breed_object.pk
#     }
#     return render(request, 'dogs/dogs.html', context=context)



