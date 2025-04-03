from django.urls import path  
from dogs.apps import DogsConfig 
from dogs.views import (
    index_view, 
    breeds_list_view, 
    breed_dogs_list_view, 
    dog_list_view,
    dog_create_view
)


app_name = DogsConfig.name  


urlpatterns = [
    # breads
    path('', index_view, name='index_view'),
    path('breeds/', breeds_list_view, name='breeds'),
    path('breeds/<int:pk>/dogs', breed_dogs_list_view, name='breed_dogs'),

    # dogs
    path('dogs/', dog_list_view, name='dogs_list'),
    path('dogs/create', dog_create_view, name='dog_create'),
]
