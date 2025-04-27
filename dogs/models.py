from django.db import models
from django.conf import settings

# Create your models here.
NULLABLE = {'blank': True, 'null': True}

# Create your models here.
class Breed(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name='Порода'
    )
    description = models.CharField(
        max_length=1000, 
        verbose_name='Описание'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'

# My metamodel 
class Dog(models.Model):
    name = models.CharField(
        max_length=250, 
        verbose_name='Кличка'
    )
    breed = models.ForeignKey(
        Breed, 
        on_delete=models.CASCADE, 
        verbose_name='Порода'
    )
    photo = models.ImageField(
        upload_to='dogs/', 
        **NULLABLE, 
        verbose_name='Фотография'
    )
    birth_date = models.DateField(
        **NULLABLE, 
        verbose_name='Дата рождения'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        **NULLABLE, 
        verbose_name='Хозяин'
    )

    def __str__(self):
        return f'{self.name} ({self.breed})'

    class Meta: 
        verbose_name = 'dog'
        verbose_name_plural = 'dogs'


class DogParent(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='Кличка Родителя')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name='Порода родителя')
    birth_date = models.DateField(**NULLABLE, verbose_name='Дата рождения родителя')

    def __str__(self):
        return f'{self.name} ({self.breed})'

    class Meta:
        verbose_name = 'parent'
        verbose_name_plural = 'parents'
        # abstract = True 
        # app_lable = 'dogs'
        # ordering = [-1]
        # proxy = True 
        # permissions = []
        # db_table = 'doggies'
        # get_latest_by = 'birth_date'
