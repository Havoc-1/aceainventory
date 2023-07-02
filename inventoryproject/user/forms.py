from django import forms
from django.contrib.auth.models import User
from django.apps import apps
from dashboard.models import Location
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')                  #  '__all__' if you want to see all

class EditLocation(UserChangeForm):
    password = None

    class Meta:
        model = UserProfile
        exclude = ['password']
        fields = ['location']

class EditProfileForm(UserChangeForm):
    password = None

    class Meta: #specifying meta data
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'last_name', 'email')   
        
class ImageUpdateForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ['image']