from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login ,logout  # Rename login function here

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please choose a different username.")
        else:
            # Create the new user
            my_user = User.objects.create_user(username, email, password)
            my_user.save()
            return redirect('login')
        
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use auth_login instead of login here
            return redirect('home')
        else:
            return render(request, 'login_failed.html') 
            
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def authentication_required(function=None, redirect_field_name=signup, login_url=login):
    actual_decorator = login_required(function, redirect_field_name, login_url)

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return actual_decorator(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(login_url))

    return wrapper

@authentication_required
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request,'about.html')