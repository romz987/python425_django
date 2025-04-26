import datetime
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

    def clean_birth_date(self):
        cleaned_data = self.cleaned_data.get('birth_date')
        if cleaned_data:
            now_year = datetime.datetime.now().year 
            if now_year - cleaned_data.year > 35:
                raise forms.ValidationError(
                    'Собака должна быть моложе 35 лет'
                )
        return cleaned_data

