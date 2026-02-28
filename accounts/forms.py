from django.forms import ModelForm
from .models import User

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password1']
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get('password')
    #     password1 = cleaned_data.get('password1')

    #     if password and password1 and password != password1:
    #         self.add_error('password1', 'Passwords do not match.')

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']