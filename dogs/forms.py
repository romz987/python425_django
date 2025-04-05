from django import forms 
from dogs.models import Dog 
from django.forms import DateInput


class DogForm(forms.ModelForm):
    
    class Meta:
        model = Dog 
        fields = '__all__'
        # Используем виджет date
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'})          
        }

