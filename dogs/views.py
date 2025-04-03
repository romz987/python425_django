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
