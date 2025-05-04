import datetime
from django import forms 
from dogs.models import Dog, DogParent
from django.forms import DateInput

from users.forms import StyleFormMixin


class DogForm(StyleFormMixin, forms.ModelForm):
    
    class Meta:
        model = Dog 
        fields = '__all__'
        exclude = ('owner', )
        # Используем виджет date
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
                # Если явно не указать формат то не работает
                format='%Y-%m-%d'
            )
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



class DogParentForm(StyleFormMixin, forms.ModelForm):
    class Meta: 
        model = DogParent
        fields = '__all__'
