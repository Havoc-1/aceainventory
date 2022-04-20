from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']                   #  '__all__' if you want to see all

class EditProfileForm(UserChangeForm):
    class Meta: #specifying meta data
        model = User
        fields = [      #fields to include
            'username',
            'first_name',
            'last_name',
            'email',
        ] 
        
class ImageUpdateForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ['image']