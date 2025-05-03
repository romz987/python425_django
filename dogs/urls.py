from django.urls import path  
from dogs.apps import DogsConfig 
from dogs.views import (
    BreedDogsListView,
    IndexView,
    BreedsListView,
    DogDeleteView,
    DogCreateView,
    DogUpdateView,
    DogDetailView,
    DogListView
)
# Redis  
from django.views.decorators.cache import cache_page


app_name = DogsConfig.name  


urlpatterns = [
    # breads
    path('', cache_page(60)(IndexView.as_view()), name='index'),
    path('breeds/', cache_page(60)(BreedsListView.as_view()), name='breeds'),    
    path('breeds/<int:pk>/dogs', cache_page(60)(BreedDogsListView.as_view()), name='breed_dogs'),

    # dogs
    path('dogs/', cache_page(60)(DogListView.as_view()), name='dogs_list'),
    path('dogs/create', cache_page(60)(DogCreateView.as_view()), name='dog_create'),
    path('dogs/detail/<int:pk>/', cache_page(60)(DogDetailView.as_view()), name='dog_detail'),
    path('dogs/update/<int:pk>/', cache_page(60)(DogUpdateView.as_view()), name='dog_update'),
    path('dogs/delete/<int:pk>/', cache_page(60)(DogDeleteView.as_view()), name='dog_delete')
]
