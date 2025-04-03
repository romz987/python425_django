from django.urls import path  
from dogs.apps import DogsConfig 
from dogs.views import index 


app_name = DogsConfig.name  


urlpatterns = [
    path('', index, name='index_view')
]
