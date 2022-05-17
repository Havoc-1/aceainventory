from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm   # django making life easier
from .forms import CreateUserForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
#to make sure user is still logged in after redirect in change password
from django.contrib.auth import update_session_auth_hash 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

# Create your views here.

class customLoginView(auth_views.LoginView):            # redirects the user back to dashboard index when going back to login even though they are logged in already
    template_name ='user/login.html'
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard-index')) 
        else: 
            return super(customLoginView, self).dispatch(*args, request, **kwargs)
    

def register(request):
    if request.user.is_authenticated:                   
        return redirect(reverse('dashboard-index'))             # redirects the user back to dashboard index when going back to login even though they are logged in already
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

@login_required
def view_profile(request):
    #context = {'username': request.user, 'fname': request.user.first_name, 'lname': request.user.last_name, 'email': request.user.email} # dictionary to call information
    return render(request, 'user/profile.html') #, context

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user) #passing user instance so it knows the user object
        if form.is_valid():
            form.save()
            return redirect('view-profile')
    else: # for the GET, init blank form
        form = EditProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'user/edit_profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user) #django requires user to be called
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) #grab the user that changed their password using the form
            return redirect('view-profile')
        else: #form data invalid
            return redirect('password') 
    else: # for the GET, init blank form
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'user/change_password.html', context)