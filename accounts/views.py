from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Registration view
def register_view(request):
    if request.user.is_authenticated:
        return redirect('leetcode:roadmap') 
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Error creating account. Please check your information.')
    else:
        form = UserCreationForm()

    # Add form-control class to each field
    form.fields['username'].widget.attrs.update({'class': 'form-control'})
    form.fields['password1'].widget.attrs.update({'class': 'form-control'})
    form.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    return render(request, 'accounts/register.html', {'form': form})
def login_view(request):
    if request.user.is_authenticated:
        # If the user is already logged in, redirect to the home page
        return redirect('home')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user if authentication is successful
            login(request, user)
            # messages.success(request, "Login successful!")
            return redirect('leetcode:roadmap')   # Redirect to homepage after successful login
        else:
            # Show error message if login fails
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'accounts/login.html')

@login_required
def home_view(request):
    
    return redirect('leetcode:roadmap',username=user) 


def logout_view(request):
    logout(request)
    return redirect('login')

