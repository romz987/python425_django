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


app_name = DogsConfig.name  


urlpatterns = [
    # breads
    path('', IndexView.as_view(), name='index'),
    path('breeds/', BreedsListView.as_view(), name='breeds'),
    path('breeds/<int:pk>/dogs', BreedDogsListView.as_view(), name='breed_dogs'),

    # dogs
    path('dogs/', DogListView.as_view(), name='dogs_list'),
    path('dogs/create', DogCreateView.as_view(), name='dog_create'),
    path('dogs/detail/<int:pk>/', DogDetailView.as_view(), name='dog_detail'),
    path('dogs/update/<int:pk>/', DogUpdateView.as_view(), name='dog_update'),
    path('dogs/delete/<int:pk>/', DogDeleteView.as_view(), name='dog_delete')
]
