from django.shortcuts import render, get_object_or_404

# My imports 
from dogs.models import Breed, Dog
from django.http import HttpResponseRedirect 
from django.urls import reverse 
from dogs.forms import DogForm 

# Только авторизованные пользователи 
from django.contrib.auth.decorators import login_required

# Create your views here.
def index_view(request):
    context = {        
        'objects_list': Breed.objects.all()[:3],
        'title': 'Питомник - Главная страница'
    }
    return render(request, 'dogs/index.html', context=context)


# отображение всех объектов независимо от модели 
def breeds_list_view(request):
    context = {
        'objects_list': Breed.objects.all(),
        'title': 'Питомник - Все наши породы'
    }
    return render(request, 'dogs/breeds.html', context=context)


def breed_dogs_list_view(request, pk: int):
    breed_object = Breed.objects.get(pk=pk)
    context = {
        'objects_list': Dog.objects.filter(breed_id=pk),
        'title': f'Собаки породы - {breed_object}',
        'breed_pk': breed_object.pk
    }
    return render(request, 'dogs/dogs.html', context=context)


def dog_list_view(request):
    context = {
        'objects_list': Dog.objects.all(),
        'title': f'Все наши собаки',
    }   
    return render(request, 'dogs/dogs.html', context)


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


@login_required(login_url='users:user_login')
def dog_create_view(request):
    """ Создать собаку """
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog_object = form.save()
            dog_object.owner = request.user 
            dog_object.save()
            #form.save()
            return HttpResponseRedirect(reverse('dogs:dogs_list'))
        else:
            print(form.errors)  # Добавьте эту строку для отладки
    else:
        form = DogForm()

    context = {
        'title': 'Добавить собаку',
        'form': form
    }
    return render(request, 'dogs/create_update.html', context=context)


@login_required(login_url='users:user_login')
def dog_detail_view(request, pk):
    """ Вернуть детальную информацию о собаке """
    dog_object = Dog.objects.get(pk=pk)
    context = {
        'object': dog_object,
        'title': dog_object.name + ' - ' + dog_object.breed.name
    }
    return render(request, 'dogs/detail.html', context=context)


@login_required(login_url='users:user_login')
def dog_update_view(request, pk):
    """ Изменить информацию о собаке """
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST': 
        form = DogForm(request.POST, request.FILES, instance=dog_object)
        if form.is_valid():
            dog_object = form.save()
            dog_object.save()
            return HttpResponseRedirect(reverse('dogs:dog_detail', args={pk:pk}))
    context = {
        'title': 'Изменить собаку',
        'object': dog_object,
        'form': DogForm(instance=dog_object)
    }
    return render(request, 'dogs/create_update.html', context=context)


@login_required(login_url='users:user_login')
def dog_delete_view(request, pk):
    """ Удалить собаку """
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        dog_object.delete()
        return HttpResponseRedirect(reverse('dogs:dogs_list'))
    context = {
        'object': dog_object,
        'title': 'Удалить собаку'
    }
    return render(request, 'dogs/delete.html', context=context)
