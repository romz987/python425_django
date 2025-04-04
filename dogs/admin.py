from django.contrib import admin
from dogs.models import Breed, Dog

# Register your models here.
# Breed
@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    ordering = ('pk', )


# Dog
@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    # поля, которые будут отображатсья в админке
    list_display = ('pk', 'name', 'breed')
    # поля, по которым можно будет сортировать объекты модели в админке
    list_filter = ('breed', )
    # как будут сортироваться объекты модели в административной панели
    # по полю 'name' в данном случае
    ordering = ('name', )
