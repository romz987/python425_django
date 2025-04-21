from django import forms 
from dogs.models import Dog 
from django.forms import DateInput

from users.forms import StyleFormMixin


class DogForm(StyleFormMixin, forms.ModelForm):
    
    class Meta:
        model = Dog 
        exclude = ('owner', )
        # fields = '__all__'
        # Используем виджет date
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'})          
        }

