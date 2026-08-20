from django.shortcuts import render,redirect
from .models import Formation, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
import json
from cart.cart import Cart

# Create your views here.
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()

            messages.success(request, "Your Profile has been updated!!")
            return redirect('update_info')
        return render(request, "update_info.html", {'form':form})
    else:
        messages.success(request, "You must be Logged in to access this page!!")
        return redirect('home')

def search(request):
    #Determine if user filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        #Query The Formation DB Model
        searched = Formation.objects.filter(titre__icontains=searched)
        #TEST for null
        if not searched:
           messages.success(request, "No such Formation in our Koursero!")
           return render(request, 'search.html', {"searched":searched})
        else:
            return render(request, 'search.html', {"searched":searched})
    else:

        return render(request, 'search.html', {})

def formation(request,pk):
    formation = Formation.objects.get(id=pk)
    return render(request, 'formation.html', {'formation':formation})

def home(request):
    formations = Formation.objects.all()
    return render(request, 'home.html', {'formations':formations})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #for the cart
            current_user = Profile.objects.get(user__id=user.id)
            #get their saved cart from database
            saved_cart = current_user.old_cart
            #convert DB string to python dictionary
            if saved_cart:
                #convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #add loaded cart dictionary to our session
                cart = Cart(request)
                #loop through the cart and add items from the database
                for key, price in converted_cart.items():
                    cart.db_add(formation_id=key, price=price)

            messages.success(request, "You have been logged in!")  
            return redirect('home')
        else:
            messages.error(request, "There was an error, please try again..") 
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User Profile has been updated!!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You must be Logged in to access this page!!")
        return redirect('home')
    
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ChangePasswordForm


def update_password(request):
    current_user = request.user
    
    if request.method == 'POST':
        form = ChangePasswordForm(current_user, request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been updated. Please log in again.")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = ChangePasswordForm(current_user)
    
    # Ensure we always return an HttpResponse
    return render(request, 'update_password.html', {'form': form})

    

def logout_user(request):
    # code de traitement de connexion 
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered successfully !")
            return redirect('update_info')
        else:
            messages.error(request, "There was an error, please try again..")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

