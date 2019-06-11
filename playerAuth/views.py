from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from playground.models import Player
from django.conf import settings

def Signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.last()
            login(request, user)
            Player.objects.create(
                user = user,
            )
            print("boo")
            return redirect('playground:index')
    else:
        form = UserCreationForm()
    return render(request, 'playerAuth/signup_page.html', {'form':form})

def Login(request):
    if request.method ==  'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('playground:index')
    else:
        form = AuthenticationForm()
    return render(request, 'playerAuth/login_page.html', {'form':form})
    
def loggedout(request):
    # if request.user.is_authenticated:
    logout(request)
    return redirect('playerAuth:login')

def google_login(request):
    if request.user.is_authenticated:
        # User.objects.get(username = request.user.username)
        try:
            Player.objects.get(user = request.user)
        except ObjectDoesNotExist:
            Player.objects.create(
                user = request.user,
            )
            Player.save()
        return redirect('playground:index')
    return redirect('social:begin', 'google-oauth2')

