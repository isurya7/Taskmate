from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomRegisterForm
from django.contrib.auth import authenticate,login,logout

def register(request):
    if request.method == "POST":
        register_form = CustomRegisterForm(request.POST)
        if register_form.is_valid():
            # Save the form only if it is valid
            register_form.save()
            username = register_form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}. Login to create a task!")
            return redirect('todolist')    
    else:
        # Create a new form instance when the request method is not POST
        register_form = CustomRegisterForm()

    return render(request, 'register.html', {'register_form': register_form})


def login_user(request): 
    if request.method=="POST":
        username=request.POST['username'] 
        password=request.POST['password']  
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, f"Hey {username}! welcome to Taskmate.")
            return redirect('todolist')
        else:
            messages.success(request,"Incorrect password or username please try again.")
            return redirect('login')

    else:
        return render(request, "login.html", {}) 

    


def logout_user(request):
    logout(request)
    return redirect('home')
