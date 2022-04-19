from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm   # django making life easier
from .forms import CreateUserForm

# Create your views here.
def register(request):
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():             # does data validation for us
            form.save()                 # django making life easier
            return redirect('user-login')       # redirects to login page after succesful user registration
    else:
        form = CreateUserForm()
    context = {
        'form':form,
        
    }
    return render(request, 'user/register.html', context)    # (request, templateLocation, {context})