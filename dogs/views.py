from django.shortcuts import render

# My imports 
from dogs.models import Breed, Dog 

# Create your views here.
def index_view(request):
    context = {        
        'objects_list': Breed.objects.all()[:3],
        'title': 'Питомник - Главное'
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
        'title': f'Собаки породы - {Breed.objects.name}',
        'breed_pk': breed_object.pk
    }
    return render(request, 'dogs/dogs.html', context=context)
