from django import forms 

from users.models import User 


class UserRegisterForm(forms.ModelForm):

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    
    class Meta: 
        model = User 
        fields = ('email', )


    def clean_password2(self):
        cleaned_data = self.cleaned_data 
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают!!!')
        return cleaned_data['password2']


class UserLoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

